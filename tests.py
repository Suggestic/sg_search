from sg_search import SGSearch

search = SGSearch('localhost:9202')
result = search.product('Cabernet Sauvignon, Faust 11 Napa', 'Cabernet Sauvignon')
# result2 = search.meal("2000 Meritage, Opus One, Napa", "")
# recipes = search.recipe_by_token('bread', 2)
