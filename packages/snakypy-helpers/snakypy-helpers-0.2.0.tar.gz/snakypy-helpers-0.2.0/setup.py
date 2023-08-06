# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snakypy',
 'snakypy.helpers',
 'snakypy.helpers.ansi',
 'snakypy.helpers.calcs',
 'snakypy.helpers.catches',
 'snakypy.helpers.console',
 'snakypy.helpers.decorators',
 'snakypy.helpers.files',
 'snakypy.helpers.os',
 'snakypy.helpers.path',
 'snakypy.helpers.subprocess']

package_data = \
{'': ['*']}

install_requires = \
['pyfiglet==0.8.post1']

setup_kwargs = {
    'name': 'snakypy-helpers',
    'version': '0.2.0',
    'description': 'Snakypy Helpers is a package that contains code ready to assist in the development of packages/applications so as not to replicate the code.',
    'long_description': '================\nSnakypy Helpers\n================\n\n.. image:: https://github.com/snakypy/snakypy-helpers/workflows/Tests/badge.svg\n    :target: https://github.com/snakypy/snakypy-helpers\n    :alt: Tests\n\n.. image:: https://img.shields.io/pypi/v/snakypy-helpers.svg\n    :target: https://pypi.python.org/pypi/snakypy-helpers\n    :alt: PyPI - Snakypy Helpers\n\n.. image:: https://img.shields.io/pypi/wheel/snakypy-helpers\n    :target: https://pypi.org/project/wheel/\n    :alt: PyPI - Wheel\n\n.. image:: https://img.shields.io/pypi/pyversions/snakypy-helpers\n    :target: https://pyup.io/repos/github/snakypy/snakypy-helpers/\n    :alt: Python versions\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Black\n\n.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n    :target: https://pycqa.github.io/isort/\n    :alt: Isort\n\n.. image:: http://www.mypy-lang.org/static/mypy_badge.svg\n    :target: http://mypy-lang.org/\n    :alt: Mypy\n\n.. image:: https://readthedocs.org/projects/snakypy-helpers/badge/?version=latest\n    :target: https://snakypy-helpers.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://pyup.io/repos/github/snakypy/snakypy-helpers/shield.svg\n    :target: https://pyup.io/repos/github/snakypy/snakypy-helpers/\n    :alt: Updates\n\n.. image:: https://img.shields.io/github/contributors/snakypy/snakypy-helpers\n    :target: https://github.com/snakypy/snakypy-helpers/blob/master/CONTRIBUTING.rst\n    :alt: Contributors\n\n.. image:: https://img.shields.io/github/issues-raw/snakypy/snakypy-helpers\n   :target: https://github.com/snakypy/snakypy-helpers/issues\n   :alt: GitHub issues\n\n.. image:: https://img.shields.io/github/license/snakypy/snakypy-helpers\n    :target: https://github.com/snakypy/snakypy-helpers/blob/master/LICENSE\n    :alt: Github License\n\n\nSnakypy Helpers is a package that contains code ready to assist in the development of Snakypy projects,\nso as not to replicate the code.\n\n\nDonation\n--------\n\nIf you liked my work, buy me a coffee <3\n\n.. image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif\n    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YBK2HEEYG8V5W&source\n\nLicense\n--------\n\nThe project is available as open source under the terms of the `MIT license`_ © William Canin\n\nCredits\n--------\n\nSee in `AUTHORS`_.\n\nLinks\n-----\n\n* Code: https://github.com/snakypy/snakypy-helpers\n* Documentation: https://snakypy-helpers.readthedocs.io\n* Releases: https://pypi.org/project/snakypy-helpers/#history\n* Issue tracker: https://github.com/snakypy/snakypy-helpers/issues\n\n.. _MIT license: https://github.com/snakypy/snakypy-helpers/blob/master/LICENSE\n.. _AUTHORS: https://github.com/snakypy/snakypy-helpers/blob/master/AUTHORS.rst\n',
    'author': 'William C. Canin',
    'author_email': 'william.costa.canin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/snakypy/snakypy-helpers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
