# SG Search

**Note this package is on development**

```
pip install -e .
```

```
from sg_search import SGSearch

search = SGSearch('localhost:9202')
result = search.find_meal('cabernet sauvignon, faust 11 napa', 'cabernet sauvignon')

print(result)
```