# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tomli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tomli',
    'version': '0.2.0',
    'description': "A lil' TOML parser",
    'long_description': '[![Build Status](https://github.com/hukkinj1/tomli/workflows/Tests/badge.svg?branch=master)](https://github.com/hukkinj1/tomli/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)\n[![codecov.io](https://codecov.io/gh/hukkinj1/tomli/branch/master/graph/badge.svg)](https://codecov.io/gh/hukkinj1/tomli)\n[![PyPI version](https://img.shields.io/pypi/v/tomli)](https://pypi.org/project/tomli)\n\n# Tomli\n\n> A lil\' TOML parser\n\nTomli is a Python library for parsing [TOML](https://toml.io).\nTomli is fully compatible with [TOML v1.0.0](https://toml.io/en/v1.0.0).\n\n## Installation\n\n```bash\npip install tomli\n```\n\n## Usage\n\n### Parse a TOML string\n\n```python\nimport tomli\n\ntoml_str = """\ngretzky = 99\n\n[kurri]\njari = 17\n"""\n\ntoml_dict = tomli.loads(toml_str)\nassert toml_dict == {"gretzky": 99, "kurri": {"jari": 17}}\n```\n\n### Handle invalid TOML\n\n```python\nimport tomli\n\ntry:\n    toml_dict = tomli.loads("]] this is invalid TOML [[")\nexcept tomli.TOMLDecodeError:\n    print("Yep, definitely not valid.")\n```\n\n## FAQ\n\n### Why this parser?\n\n- it\'s lil\'\n- fairly fast (but pure Python so can\'t do any miracles there)\n- 100% spec compliance: passes all tests in [a test set](https://github.com/toml-lang/compliance/pull/8) soon to be merged to the official [compliance tests for TOML](https://github.com/toml-lang/compliance) repository\n\n### Is comment preserving round-trip parsing supported?\n\nNo. The `tomli.loads` function returns a plain `dict` that is populated with builtin types and types from the standard library only\n(`list`, `int`, `str`, `datetime.datetime` etc.).\nPreserving comments requires a custom type to be returned so will not be supported,\nat least not by the `tomli.loads` function.\n\n### Is there a `dumps`, `write` or `encode` function?\n\nNot yet, and it\'s possible there never will be.\n',
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/tomli',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
