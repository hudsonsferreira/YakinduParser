=============
YakinduParser(YP)
=============

Detects Finite-State Machine in a requirements description.
The goal of YP is to induce a new way to avoid ambiguity in software requirements.

Requeriments description in a .odt format:

(You can found it in the resources directory)


![Alt text] (/parser/spec/resources/images/refrigerator_requirements.png)

As a dependency you must copy the some nltk_data modules do your home. You can run the bellow code:
```
cd YakinduParser

cp -r nltk_data ~/
```


Installing:
```
[sudo] python setup.py install
```
Running tests:
```
specloud
```

Usage:
```python
from yakinduparser import YakinduParser
parser = YakinduParser('/spec/resources/refrigerator.odt')
parser.create_class_factory_utils()
```
