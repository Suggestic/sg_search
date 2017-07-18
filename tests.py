from sg_search import SGSearch

search = SGSearch('localhost:9202')
# result = search.meal('cabernet sauvignon, faust 11 napa', 'cabernet sauvignon')
# result2 = search.meal("2000 Meritage, Opus One, Napa", "")
recipes = search.recipe_by_token('bread', 2)
