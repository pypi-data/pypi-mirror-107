# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rubric']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['rubric = rubric.rubric:cli_entrypoint']}

setup_kwargs = {
    'name': 'rubric',
    'version': '0.1.3',
    'description': 'Initialize your Python project with all the linting boilerplates you need',
    'long_description': '## Preface\n\nRubric is an opinionated project initializer for Python. Following is a list of config files that rubric is going to add to your directory:\n\n```\n├── .flake8\n├── .gitignore\n├── makefile\n├── mypy.ini\n├── pyproject.toml\n├── README.md\n├── requirements-dev.txt\n├── requirements.in\n└── requirements.txt\n```\n\n\n## Installation\n\n* Make a virtual environment in your project\'s root director.\n\n* Activate the environemnt and run:\n\n    ```\n    pip install rubric\n    ```\n\n## Usage\n\n* To inspect all the CLI options, run:\n\n    ```\n    rubric --help\n    ```\n\n    You should see the following output:\n\n    ```\n    $ rubric\n\n           ___       __       _\n          / _ \\__ __/ /  ____(_)___\n         / , _/ // / _ \\/ __/ / __/\n        /_/|_|\\_,_/_.__/_/ /_/\\__/\n\n    usage: rubric [-h] [--dirname DIRNAME] [--overwrite] run\n\n    Rubric -- Initialize your Python project ⚙️\n\n    positional arguments:\n    run                run rubric & initialize the project scaffold\n\n    optional arguments:\n    -h, --help         show this help message and exit\n    --dirname DIRNAME  target directory name\n    --overwrite        overwrite existing linter config files\n\n    ```\n\n* Initialize your project with the following command:\n\n    ```\n    rubric run\n    ```\n\n    This will run the tool in a non-destructive way—that means it won\'t overwrite any of the configuration file that you might have in the directory.\n\n    If you want to overwrite any of the existing config file that you might have in the directory, then run:\n\n    ```\n    rubric run --overwrite\n    ```\n\n    You can also point Rubric at a directory.\n\n    ```\n    rubric run --directory="some/custom/directory"\n    ```\n',
    'author': 'rednafi',
    'author_email': 'redowan.nafi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rednafi/rubric',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
