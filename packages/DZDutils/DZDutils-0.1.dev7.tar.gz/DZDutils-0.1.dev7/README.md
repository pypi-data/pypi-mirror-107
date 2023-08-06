# DZDuitls

Python tool collection

## About

**Maintainer**: tim.bleimehl@dzd-ev.de

**Licence**: MIT

**Purpose**:

TODO


## Install

pip3 install git+https://git.connect.dzd-ev.de/dzdpythonmodules/dzdutils.git


## Modules

### DZDutils.inspect

**object2html**

Opens the webbrowser and let you inspect any object / dict with jquery jsonviewer

```python
from DZDutils.inspect import object2html
my_ultra_complex_dict = {"key":"val"}
object2html(my_ultra_complex_dict)
``` 

### DZDutils.list

**chunks**

Breaks up a list in shorter lists and yields shorter lists

```python
from DZDutils.list import chunks
my_ultra_long_list = [1,2,3,4,5,6,7,8,9,10]
for chunk in chunks(my_ultra_long_list, 3)
    print(chunk)
```

Output:

```python
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]
[10]
``` 
### DZDutils.neo4j


**wait_for_db_boot** 

Wait for a neo4j to boot up. If timeout is expired it will raise the last error of the connection expception for debuging.
The argument `neo4j` must be a dict of py2neo.Graph() arguments -> https://py2neo.org/2021.1/profiles.html#individual-settings

```
from DZDutils.neo4j import wait_for_db_boot
wait_for_db_boot(neo4j={"host": "localhost"}, timeout_sec=120)
```