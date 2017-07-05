from sg_search import SGSearch

search = SGSearch('localhost:9200')
result = search.find_meal('cabernet sauvignon, faust 11 napa', 'cabernet sauvignon')

print(result)
