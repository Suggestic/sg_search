import os
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search, Q
from slugify import slugify

ELASTICSEARCH = os.environ.get('ELASTICSEARCH')
RECIPE_INDEX = 'recipes_v1'
PRODUCT_INDEX = 'product_v1'

# `empty_results.result.src` is set depending function called
# Example:
# empty_results["result"][0]["src"] = 'pm'
# empty_results["result"][0]["src"] = 'rm'
empty_results = {
    "result": [
        {
            "ings": [],
            "ings_scores": [],
            "courses": [],
            "courses_scores": [],
            "name": None,
            "nutrients": [],
            "trust_me": False,
        }
    ]
}


def clean_name(name):
    name = name.replace('&', 'and')
    return slugify(
        name, save_order=True, word_boundary=False, separator=" "
    )


class SGSearch(object):
    def __init__(self, elasticsearch=None, **kwargs):
        # If no elasticsearch provided, fallback to $ELASTICSEARCH.
        self.elasticsearch = elasticsearch

        if not self.elasticsearch:
            raise ValueError('You must provide a elasticsearch host.')

        self.elasticsearch_connection = connections.configure(
            default={'hosts': self.elasticsearch, 'timeout': 20}, sniff_on_start=True
        )

    def __repr__(self):
        return '<SGsearch {}>'.format(self)

    def meal(self, name, simple_name):
        """
        Returns a product or recipe that matches name or simple_name

        @simple_name: hamburger
        @name: hamburger with cheese
        """
        query = Search(index='{},{}'.format(RECIPE_INDEX, PRODUCT_INDEX))

        # product queries
        nested_product_course_name = Q(
            'nested', path='scoring.courses', query=Q(
                'term', scoring__courses__name="Wine"
            ) & Q(
                'exists', field="scoring.ingredients"
            )
        )
        product_course = Q(
            'indices',
            indices=[PRODUCT_INDEX], query=nested_product_course_name
        )
        product_should_simple_name = Q(
            'term',
            name_lowercase__raw={
                'value': u'{}'.format(simple_name.strip().replace('\n', '').lower()),
                'boost': 1
            }
        )
        product_should_complex_name = Q(
            'term',
            name_lowercase__raw={
                'value': u'{}'.format(name.strip().replace('\n', '').lower()),
                'boost': 2
            }
        )
        product_name_should = Q(
            'bool',
            should=[product_should_simple_name, product_should_complex_name]
        )
        product_bool_query = Q(
            'bool',
            must=[product_course, product_name_should]
        )

        # recipe queries
        recipe_must = Q("exists", field="_sg.ingredients")
        recipe_should_simple_name = Q(
            'term',
            clean_name__raw={
                'value': clean_name(simple_name),
                'boost': 3
            }
        )
        recipe_should_complex_name = Q(
            'term',
            clean_name__raw={
                'value': clean_name(name),
                'boost': 4
            }
        )
        recipe_name_should = Q(
            'bool',
            should=[recipe_should_simple_name, recipe_should_complex_name]
        )
        recipe_bool_query = Q(
            'bool',
            must=[recipe_must, recipe_name_should]
        )

        # product and recipe bool query
        query = query.query(
            'bool',
            should=[product_bool_query, recipe_bool_query],
        )

        result = query.execute()

        if result:
            nutrients = []
            index = result.hits[0].meta.index

            if index == 'product':
                _ingredients = [i.name for i in result[0].scoring.ingredients]
                _ingredients_lines = []
                src = 'pm'
                _course = [c.name for c in result[0].scoring.courses]
            else:
                _ingredients = list(result[0]._sg.ingredients) if hasattr(result[0]._sg, 'ingredients') else []
                _ingredients_lines = list(result[0].ingredientLines) if hasattr(result[0], 'ingredientLines') else []
                src = 'rm'
                _course = list(result[0].attributes.course) if hasattr(result[0].attributes, 'course') else []

            return {
                'result': [{
                    'ings': _ingredients,
                    'ings_lines': _ingredients_lines,
                    'nutrients': nutrients,
                    'courses': _course,
                    'courses_scores': [{"course": course, "score": 1.0} for course in _course],
                    'source': src,
                    'ings_scores': [{"ingredient": ing, "score": 1.0} for ing in _ingredients],
                    'name': result[0].name,
                    'trust_me': True
                }]
            }

        empty_results["result"][0]["src"] = None
        return empty_results

    def product(self, name, simple_name):
        """
        Searches for a product by name, Filters only wines and only those who
        have ingredients.

        @name: Cabernet Sauvignon, Faust 11 Napa
        @simple_name: Cabernet Sauvignon
        """
        query = Search(index=PRODUCT_INDEX)

        # Nested Query
        # filters only wine courses and products must have scoring.ingredients
        nested_scoring = [
            Q(
                'nested', path='scoring.courses',
                query=Q(
                    'term', scoring__courses__name="Wine"
                )
            ),
            Q(
                'nested', path='scoring.ingredients',
                query=Q(
                    Q('exists', field="scoring.ingredients")
                )
            )
        ]

        # Name filters
        product_should_simple_name = Q(
            'term',
            name_lowercase__raw={
                'value': u"{}".format(simple_name.strip().replace("\n", "").lower()),
                'boost': 1
            }
        )
        product_should_complex_name = Q(
            "term",
            name_lowercase__raw={
                'value': u'{}'.format(name.strip().replace("\n", "").lower()),
                'boost': 2
            }
        )

        # Bool query for product names query and nested scoring query
        query = query.query(
            'bool',
            must=nested_scoring,
            should=[product_should_simple_name, product_should_complex_name]
        )
        result = query.execute()

        if result:
            nutrients = []
            _ingredients = [i.name for i in result[0].scoring.ingredients]
            _ingredients_lines = []
            src = 'pm'
            _course = [c.name for c in result[0].scoring.courses]

            return {
                'result': [{
                    'ings': _ingredients,
                    'ings_lines': _ingredients_lines,
                    'nutrients': nutrients,
                    'courses': _course,
                    'courses_scores': [{"course": course, "score": 1.0} for course in _course],
                    'source': src,
                    'ings_scores': [{"ingredient": ing, "score": 1.0} for ing in _ingredients],
                    'name': result[0].name,
                    'trust_me': True
                }]
            }

        empty_results["result"][0]["src"] = None
        return empty_results

    def recipes(self, name):
        """
        Searches for all recipes that match by name
        @name: string name of recipe to search
        """
        query = Search(index=RECIPE_INDEX)
        recipe_must = Q("exists", field="_sg.ingredients")
        recipe_name_must = Q("term", clean_name__raw=clean_name(name))
        query = query.query(
            'bool',
            must=[recipe_must, recipe_name_must]
        )

        results = [hit.to_dict() for hit in query.scan()]
        return results

    def recipe_by_token(self, token, hits=None):
        """
        Search recipe by token
        @token: searching key word
        @hits: number of result hits to return default to all
        """
        query = Search(index=RECIPE_INDEX)
        recipe_must = Q("exists", field="_sg.ingredients")
        recipe_name_must = Q("match", clean_name=clean_name(token))
        query = query.query(
            'bool',
            must=[recipe_must, recipe_name_must]
        )
        if not hits:
            results = [hit.to_dict() for hit in query.scan()]
        else:
            results = [hit.to_dict() for hit in query[:hits].execute()]
        return results
