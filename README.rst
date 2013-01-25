YakinduParser
=============

The goal of "YakinduParser" is to detect Finite-State Machine annotations in a odt file and responsible for generates a class named FactoryUtils.java. This class is responsible for insert elements in a statechart diagram that belongs Yakindu. Yakindu Statechart Tools  is a DSL that provides an integrated modeling environment for the specification and development of reactive, event-driven systems based on the concept of statecharts. 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

 - Note: Check Yakindu website for more information: http://statecharts.org/


Installing:

    >>> [sudo] python setup.py install

Running tests:

    >>> specloud

Using:

    >>> from yakinduparser import YakinduParser
    >>> parser = YakinduParser('/spec/resources/refrigerator.odt')
    >>> parser.create_class_factory_utils()