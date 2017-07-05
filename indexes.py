from elasticsearch_dsl import DocType, Integer, Nested, Object, String, Float


class YummlyIndex(DocType):
    id = String(index='not_analyzed', copy_to='recipe_id')
    recipe_id = String(index='not_analyzed')
    name = String(fields={'raw': String(index='not_analyzed')})
    name_lowercase = String(fields={'raw': String(index='not_analyzed')})
    totalTimeInSeconds = Integer()
    rating = Integer()
    _sg = Object(properties={
        'ingredients': String(index='not_analyzed'),
        'restrictions': String(index='not_analyzed'),
        'lang': String(index='not_analyzed')
    })
    source = Object(properties={
        'sourceSiteUrl': String(index='not_analyzed'),
        'sourceDisplayName': String(index='not_analyzed'),
        'sourceRecipeUrl': String(index='not_analyzed'),
    })
    attributes = Object(properties={
        "course": String(fields={'raw': String(index='not_analyzed')})
    })
    attribution = Object(properties={
        'url': String(index='not_analyzed'),
        'text': String(index='not_analyzed'),
        'html': String(index='not_analyzed'),
        'logo': String(index='not_analyzed'),
    })
    images = Nested(properties={
        'hostedSmallUrl': String(index='not_analyzed'),
        'hostedMediumUrl': String(index='not_analyzed'),
        'hostedLargeUrl': String(index='not_analyzed')
    })
    nutrition_estimates = Object(properties={
        'protein': Float(),
        'carbs': Float(),
        'fat': Float(),
        'calories': Float()
    })

    class Meta:
        index = 'recipes_alias'
        doc_type = 'recipe'
