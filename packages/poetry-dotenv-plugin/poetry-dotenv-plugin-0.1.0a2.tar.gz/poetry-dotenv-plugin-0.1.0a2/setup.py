# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_dotenv_plugin']

package_data = \
{'': ['*'], 'poetry_dotenv_plugin': ['UNKNOWN.egg-info/*']}

install_requires = \
['poetry>=1.2.0a1', 'python-dotenv>=0.10.0']

entry_points = \
{'poetry.application.plugin': ['poetry-dotenv-plugin = '
                               'poetry_dotenv_plugin.dotenv_plugin:DotenvPlugin']}

setup_kwargs = {
    'name': 'poetry-dotenv-plugin',
    'version': '0.1.0a2',
    'description': 'A Poetry plugin to automatically load environment variables from .env files',
    'long_description': '# Poetry Dotenv Plugin\n\nA [Poetry](https://python-poetry.org/) plugin that automatically loads environment variables from `.env` files into the environment before poetry commands are run.\n\nSupports Python 3.6+\n\n```sh\n$ cat .env\nMY_ENV_VAR=\'Hello World\'\n\n$ poetry run python -c \'import os; print(os.environ.get("MY_ENV_VAR"))\'\nHello World\n```\n\nThis plugin depends on the [`python-dotenv` package](https://github.com/theskumar/python-dotenv) for its functionality and therefore also supports features that `python-dotenv` supports. Interpolating variables using POSIX variable expansion for example.\n\n### Origins\n\nInitial implementation based on the event handler application plugin example in the [Poetry docs](https://python-poetry.org/docs/plugins/#event-handler).\n\n## Install\n\n```sh\npoetry plugin add poetry-dotenv-plugin\n```\n\n### Coming from Pipenv\n\nIf you are transitioning from `pipenv` there shouldn\'t be much to change with regard to the `.env` loading. If you were a user of [`pipenv`\'s environment variables](https://pipenv.pypa.io/en/latest/advanced/#automatic-loading-of-env) to control `.env` loading then you can use the analogous environment variables listed below.\n\nPipenv env var | Poetry env var\n-------------- | ----------------------\nPIPENV_DOTENV_LOCATION | POETRY_DOTENV_LOCATION\nPIPENV_DONT_LOAD_ENV | POETRY_DONT_LOAD_ENV\n',
    'author': 'Michael Peteuil',
    'author_email': 'michael.peteuil@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mpeteuil/poetry-dotenv-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
