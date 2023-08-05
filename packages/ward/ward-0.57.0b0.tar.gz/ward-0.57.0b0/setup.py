# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ward']

package_data = \
{'': ['*']}

install_requires = \
['click-completion>=0.5.2,<0.6.0',
 'click-default-group>=1.2.2,<2.0.0',
 'click>=8.0.0,<9.0.0',
 'colorama>=0.4.0,<0.5.0',
 'cucumber-tag-expressions>=2.0.0,<3.0.0',
 'pluggy>=0.13.1,<0.14.0',
 'pprintpp>=0.4.0,<0.5.0',
 'pygments>=2.4.2,<3.0.0',
 'rich>=10.0.0,<11.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'toml>=0.10.1,<0.11.0']

extras_require = \
{':python_version == "3.6"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['ward = ward._run:run']}

setup_kwargs = {
    'name': 'ward',
    'version': '0.57.0b0',
    'description': 'A modern Python testing framework',
    'long_description': '<img src="https://user-images.githubusercontent.com/5740731/119056107-085c6900-b9c2-11eb-9699-f54ef4945623.png" width="350px">\n\n[![Codecov](https://codecov.io/gh/darrenburns/ward/branch/master/graph/badge.svg)](https://codecov.io/gh/darrenburns/ward)\n[![Documentation Status](https://readthedocs.org/projects/ward/badge/?version=latest)](https://ward.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/ward.svg)](https://badge.fury.io/py/ward)\n\n<hr>\n\n_Ward_ is a Python testing framework with a focus on productivity and readability. It gives you the tools you need to write **well-documented** and **scalable** tests.\n\n<img alt="image" src="https://user-images.githubusercontent.com/5740731/118399779-a795ff00-b656-11eb-8fca-4ceb03151f3e.png">\n\n## Features\n\nSee the full set of features in the [**documentation**](https://ward.readthedocs.io).\n\n**Descriptive test names:** describe what your tests do using strings, not function names.\n```python\n@test("1 + 2 == 3")\ndef _():\n    assert 1 + 2 == 3\n```\n\n**Modular test dependencies:** manage test setup/teardown code using fixtures that rely on Python\'s import system, not\nname matching.\n```python\n@fixture\ndef user():\n    return User(name="darren")\n    \n@test("the user is called darren")\ndef _(u=user):\n    assert u.name == "darren"\n```\n\n**Support for asyncio**: define your tests and fixtures with `async def` and call asynchronous code within them.\n\n```python\n@fixture\nasync def user():\n    u = await create_user()\n    return await u.login()\n\n@test("the logged in user has a last session date")\nasync def _(user=user):\n    last_session = await get_last_session_date(user.id)\n    assert is_recent(last_session, get_last_session_date)\n```\n\n**Powerful test selection:** limit your test run not only by matching test names/descriptions, but also on the code \ncontained in the body of the test.\n```\nward --search "Database.get_all_users"\n```\nOr use tag expressions for more powerful filtering.\n```\nward --tags "(unit or integration) and not slow"\n```\n\n**Parameterised testing:** write a test once, and run it multiple times with different inputs by writing it in a loop.\n```python\n  for lhs, rhs, res in [\n      (1, 1, 2),\n      (2, 3, 5),\n  ]:\n      @test("simple addition")\n      def _(left=lhs, right=rhs, result=res):\n          assert left + right == result\n```\n\n**Cross platform:** Tested on Mac OS, Linux, and Windows.\n\n**Speedy:** Ward\'s suite of ~320 tests run in less than half a second on my machine.\n\n**Zero config:** Sensible defaults mean running `ward` with no arguments is enough to get started. Can be configured using `pyproject.toml` or the command line if required.\n\n**Colourful, human readable output:** quickly pinpoint and fix issues with detailed output for failing tests.\n\n## Getting Started\n\nHave a look at the [**documentation**](https://ward.readthedocs.io)!\n\n## How to Contribute\n\nContributions are very welcome and encouraged!\n\nSee the [contributing guide](.github/CONTRIBUTING.md) for information on how you can take part in the development of Ward.\n',
    'author': 'Darren Burns',
    'author_email': 'darrenb900@gmail.com',
    'maintainer': 'Darren Burns',
    'maintainer_email': 'darrenb900@gmail.com',
    'url': 'https://wardpy.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
