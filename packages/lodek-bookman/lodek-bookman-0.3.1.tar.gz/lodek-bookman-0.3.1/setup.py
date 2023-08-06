# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bookman']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['bookman = bookman.bookman:main']}

setup_kwargs = {
    'name': 'lodek-bookman',
    'version': '0.3.1',
    'description': 'Small CLI tool to manage a local library.',
    'long_description': "# About\nBookman is a simple manager for books.\n\nBookman uses a convention to generate books file names.\nIt integrates with Google Books API to fetch information for a book and it generates a bookman formatted file name.\n\nCombined with `fzf` it's easy to find books.\n\nThe bookname fileconvention is as follows:\n\n```\n[tag1][tag2]Author-One,Author-Two_Book-Title(2000)_ISBN.pdf\n```\n\nTags can be used by bookman to open all books with a given tag, for instance.\n",
    'author': 'Bruno Gomes',
    'author_email': 'lodek@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lodek/bookman',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
