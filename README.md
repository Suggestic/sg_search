# SG Search

**Note:** this package is on development.

```.bash
pip install -e .
```

Create a SGSearch connection instance
```.py
from sg_search import SGSearch

search = SGSearch('localhost:9202') # host or $ELASTICSEARCH environment variable support
```

### Search for a product or recipe by name or simple name
```.py
result = search.meal(
    name='cabernet sauvignon, faust 11 napa', simple_name='cabernet sauvignon'
)
print(result)
```

### Search recipes by name
```.py
result = search.recipes('cabernet sauvignon, faust 11 napa')
print(result)
```

### Search recipe by token
```.py
# returns all hit matches `default`
recipes = search.recipe_by_token('bread')
# return only first 3 results
recipes = search.recipe_by_token('bread', 3)
```

### Search for a product by name
```.py
product = search.product('Cabernet Sauvignon, Faust 11 Napa', 'Cabernet Sauvignon')
```

**TODO:**
* Search for restaurants
* Search for menu_items
* Tests