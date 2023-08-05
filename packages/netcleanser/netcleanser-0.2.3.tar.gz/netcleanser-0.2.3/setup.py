# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netcleanser']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0',
 'purl>=1.6,<2.0',
 'requests>=2.25.1,<3.0.0',
 'tldextract>=3.1.0,<4.0.0']

setup_kwargs = {
    'name': 'netcleanser',
    'version': '0.2.3',
    'description': 'The library makes parsing and manipulation of URL🌐 and Email address📧 easy.',
    'long_description': '# netcleanser\n\nThe library makes parsing and manipulation of URL🌐 and Email address📧 easy.\n\n[![ci](https://github.com/y-bar/netcleanser/actions/workflows/ci.yml/badge.svg)](https://github.com/y-bar/netcleanser/actions/workflows/ci.yml)\n[![license](https://img.shields.io/github/license/y-bar/netcleanser.svg)](https://github.com/y-bar/netcleanser/blob/master/LICENSE)\n[![release](https://img.shields.io/github/release/y-bar/netcleanser.svg)](https://github.com/y-bar/netcleanser/releases/latest)\n[![python-version](https://img.shields.io/pypi/pyversions/netcleanser.svg)](https://pypi.org/project/netcleanser/)\n[![pypi](https://img.shields.io/pypi/v/netcleanser?color=%2334D058&label=pypi%20package)](https://pypi.org/project/netcleanser)\n\n## Install\n\n```bash\npip install netcleanser\n```\n\n## How to use\n\n### Email \n\n```python\n>>> from netcleanser import Email\n>>> email = Email(\'shinichi.takayanagi@gmail.com\')\n>>> email.domain\n\'gmail.com\'\n>>> email.local_part\n\'shinichi.takayanagi\'\n>>> email.is_valid\nTrue\n>>> email.value\n\'shinichi.takayanagi@gmail.com\'\n```\n\nThis `Email` class is `settable` and `dictable`\n```python\n# As a dict key\n>>> x = {email: 1}\n>>> x[email]\n1\n# As elemtns of set\n>>> email2 = Email("nakamichiworks@gmail.com")\n>>> {email, email, email, email2, email2}\n{Email(value=\'nakamichiworks@gmail.com)\', Email(value=\'shinichi.takayanagi@gmail.com)\'}\n```\n\n`Email.build()` allows you to create dummy email address specifing the only part of `local_part` or `domain`\n\n```python\n>>> Email.build(local_part = "hoge")\nEmail(value=\'hoge@dummy.com)\'\n>>> Email.build(domain = "hoge.com")\nEmail(value=\'dummy@hoge.com)\'\n```\n\n### Url\n\n```python\n>>> from netcleanser import Url\n>>> url = Url(\'https://www.google.com/search?q=auhuhe\')\n>>> url.scheme\n\'https\'\n>>> url.host\n\'www.google.com\'\n>>> url.domain\n\'www.google.com\'\n>>> url.registered_domain\n\'google.com\'\n>>> url.netloc\n\'www.google.com\'\n>>> url.path\n\'/search\'\n>>> url.query\n\'q=auhuhe\'\n>>> url.is_valid\nTrue\n>>> url.is_accessible\nTrue\n>>> url.value\n\'https://www.google.com/search?q=auhuhe\'\n>>> str(url)\n\'https://www.google.com/search?q=auhuhe\'\n>>> url.contains_www\nTrue\n>>> url.remove_query()\nUrl(host=\'www.google.com\', username=\'None\', password=\'None\', scheme=\'https\', port=\'None\', path=\'/search\', query=\'\', fragment=\'\')\n>>> url.remove_www()\nUrl(host=\'google.com\', username=\'None\', password=\'None\', scheme=\'https\', port=\'None\', path=\'/search\', query=\'q=auhuhe\', fragment=\'\')\n```\n\nThis `Url` class is `settable` and `dictable`\n```python\n>>> x = {url: 123}\n>>> x[Url(\'https://www.google.com/search?q=auhuhe\')]\n123\n>>> {url, url, Url(\'https://google.com\'), url}\n{Url(host=\'www.google.com\', username=\'None\', password=\'None\', scheme=\'https\', port=\'None\', path=\'/search\', query=\'q=auhuhe\', fragment=\'\'), Url(host=\'google.com\', username=\'None\', password=\'None\', scheme=\'https\', port=\'None\', path=\'\', query=\'\', fragment=\'\')}\n```\n\n## Thanks\n`Url` class strongly depends on awesome [purl](https://github.com/codeinthehole/purl) package, thanks!\n',
    'author': 'Shinichi Takayanagi',
    'author_email': 'shinichi.takayanagi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/y-bar/netcleanser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
