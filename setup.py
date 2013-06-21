from setuptools import setup, find_packages

version = '0.0.1'
readme = open('README.rst').read()

setup(name='yakinduparser',
      version=version,
      description="A parser that identifies notes at a .odt file, based on Finite-State Machine.",
      long_description=readme,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='parser odt fsm python',
      author='Hudson Ferreira, Eduardo Carvalho',
      author_email='silvaferreira.hsf@gmail.com, eduardo.oak80@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "should_dsl",
        "lxml",
        "specloud",
        "nltk",
        "python-magic",
        "ipython",
        "lettuce"
        ],
      )