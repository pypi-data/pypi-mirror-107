# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['py']
install_requires = \
['botocore<2']

setup_kwargs = {
    'name': 'aws-sqs-batchlib',
    'version': '0.1.0',
    'description': 'Library working with Amazon SQS',
    'long_description': None,
    'author': 'Sami Jaktholm',
    'author_email': 'sjakthol@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
