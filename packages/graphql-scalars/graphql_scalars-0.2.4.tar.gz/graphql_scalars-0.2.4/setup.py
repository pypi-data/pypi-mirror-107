# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphql_scalars', 'graphql_scalars.scalars']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.1.0,<1.2.0', 'graphql-core>=3.1.4,<3.2.0']

setup_kwargs = {
    'name': 'graphql-scalars',
    'version': '0.2.4',
    'description': 'A library of custom GraphQL scalar types for creating precise type-safe GraphQL schemas.',
    'long_description': '# GraphQL-Scalars\n\n> A library of custom GraphQL scalar types for creating precise type-safe GraphQL schemas.\n\n> Great appreciation to [Urigo/graphql-scalars](https://github.com/Urigo/graphql-scalars)\n\n![PyPI](https://img.shields.io/pypi/v/graphql-scalars)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/graphql-scalars)\n![PyPI - Implementation](https://img.shields.io/pypi/implementation/graphql-scalars)\n![PyPI - License](https://img.shields.io/pypi/l/graphql-scalars)\n\n[![Build Status](https://travis-ci.com/ATyped/graphql-scalars.svg?branch=master)](https://travis-ci.com/ATyped/graphql-scalars)\n[![codecov](https://codecov.io/gh/ATyped/graphql-scalars/branch/master/graph/badge.svg?token=BKHR0I84GK)](https://codecov.io/gh/ATyped/graphql-scalars)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/ATyped/graphql-scalars.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ATyped/graphql-scalars/alerts/)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ATyped/graphql-scalars.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ATyped/graphql-scalars/context:python)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/953ed7af1f1849aab25c0e036f7f42d9)](https://www.codacy.com/gh/ATyped/graphql-scalars/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ATyped/graphql-scalars&amp;utm_campaign=Badge_Grade)\n\n## Getting Started\n\n\\# TODO\n\n## License\n\nReleased under the [MIT license](./LICENSE).\n',
    'author': 'iyanging',
    'author_email': 'iyanging@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
