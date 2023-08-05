# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyelegantsdds', 'pyelegantsdds.tools']

package_data = \
{'': ['*']}

install_requires = \
['PyNAFF>=1.1.4,<2.0.0',
 'dask>=2021.4.1,<2022.0.0',
 'ipykernel>=5.5.4,<6.0.0',
 'ipython>=7.23.1,<8.0.0',
 'isort>=5.8.0,<6.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'nbsphinx>=0.8.4,<0.9.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pandoc>=1.0.2,<2.0.0',
 'scipy>=1.6.3,<2.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'tqdm>=4.60.0,<5.0.0']

setup_kwargs = {
    'name': 'pyelegantsdds',
    'version': '0.1.1',
    'description': '<Enter a one-sentence description of this project here.>',
    'long_description': '=============\nPyElegantSDDS\n=============\n\n\nPyElegantSDDS is a Python wrapper around a Singularity container with SDDS and Parallel\nElegant installed in it. It uses this container to build and run templates for common task in \nparticle tracking for accelerators.\n\n* Free software: MIT license\n* Documentation: https://PyElegantSDDS.readthedocs.io.\n\n\nFeatures\n--------\n\n* SDDS commands\n* Elegant commands (twiss, track, FMA, DA, ...)\n* Run simulations in just a few lines of Python code. \n* Generate Hyper-cubical and Hyper-Spherical distributions for tracking\n* Quick plotting using SDDS tools\n\n',
    'author': 'Tom Mertens',
    'author_email': 'your.email@whatev.er',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tomerten/PyElegantSDDS',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
