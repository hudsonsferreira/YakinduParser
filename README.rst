=============
YakinduParser
=============

The goal of "YakinduParser" is to detect Finite-State Machine annotations in a odt file and responsible for generates a class named FactoryUtils.java. This class is responsible for insert elements in a statechart diagram that belongs Yakindu. Yakindu Statechart Tools  is a DSL that provides an integrated modeling environment for the specification and development of reactive, event-driven systems based on the concept of statecharts.

- Note: Check Yakindu website for more information: http://statecharts.org/


Installing:
- Note: As a dependency you must have installed NLTK-Trainer and take care of the path that makes references to the tagger conll2000_aubt.pickle in  in yakinduparser.py file, check NLTK-Trainer documentation to understand it better: http://nltk-trainer.readthedocs.org/en/latest/train_tagger.html
    
    >>> [sudo] python setup.py install

Running tests:
    >>> specloud

Using:
    >>> from yakinduparser import YakinduParser
    >>> parser = YakinduParser('/spec/resources/refrigerator.odt')
    >>> parser.create_class_factory_utils()