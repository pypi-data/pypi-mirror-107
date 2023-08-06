# Compact

[PHP compact() ported to Python](https://www.php.net/manual/en/function.compact.php)  
(Please use this for development only!)

```python
from compact import compact

a = 1
b = 2
c = compact(a, 'b')
# -> {'a': 1, 'b': 2}

compact(c, 
        d, 
        dirty=True)
# -> {c: {'a': 1, 'b': 2}, d: None}
```

Only works in scripts, not interactive use 
(the program needs to be able to read the source files)