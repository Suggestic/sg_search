from sg_search import SGSearch

search = SGSearch('104.198.231.232:9202')
results = search.find_meal('cabernet sauvignon, faust 11 napa', 'cabernet sauvignon')

print results
