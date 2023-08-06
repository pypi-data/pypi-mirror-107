# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idl2js', 'idl2js.js', 'idl2js.webidl', 'idl2js.webidl.generated']

package_data = \
{'': ['*']}

install_requires = \
['antlr4-python3-runtime>=4.9.2,<5.0.0',
 'attrs>=19.3.0,<20.0.0',
 'click>=7.1.2,<8.0.0',
 'graphviz>=0.16,<0.17',
 'more_itertools>=8.4.0,<9.0.0',
 'stringcase>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'idl2js',
    'version': '0.1.0',
    'description': 'Grammar-based Fuzzer that uses WebIDL as a grammar.',
    'long_description': '# idl2js\n\n[![Build Status](https://img.shields.io/travis/PrVrSs/idl2js/master?style=plastic)](https://travis-ci.org/github/PrVrSs/idl2js)\n[![Codecov](https://img.shields.io/codecov/c/github/PrVrSs/idl2js?style=plastic)](https://codecov.io/gh/PrVrSs/idl2js)\n[![Python Version](https://img.shields.io/badge/python-3.9-blue?style=plastic)](https://www.python.org/)\n[![License](https://img.shields.io/cocoapods/l/A?style=plastic)](https://github.com/PrVrSs/idl2js/blob/master/LICENSE)\n\n\n## Quick start\n\n```shell script\npip install idl2js\n```\n\n\n### Links\n\n\n* [searchfox - webidl](https://searchfox.org/mozilla-central/source/dom/webidl)\n* [original webidl parser](https://github.com/w3c/webidl2.js)\n* [TSJS-lib-generator](https://github.com/microsoft/TSJS-lib-generator/tree/master/inputfiles/idl)\n* [ECMAScript® 2021 Language Specification](https://tc39.es/ecma262/)\n\n\n## Contributing\n\nAny help is welcome and appreciated.\n\n\n## License\n\n*idl2js* is licensed under the terms of the Apache-2.0 License (see the file LICENSE).\n',
    'author': 'Sergey Reshetnikov',
    'author_email': 'resh.sersh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PrVrSs/idl2js',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
