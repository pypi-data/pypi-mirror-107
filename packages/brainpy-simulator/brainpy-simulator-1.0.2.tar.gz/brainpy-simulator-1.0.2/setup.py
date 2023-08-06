# -*- coding: utf-8 -*-

import io
import os
import re

from setuptools import find_packages
from setuptools import setup

# version
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'brainpy', '__init__.py'), 'r') as f:
    init_py = f.read()
version = re.search('__version__ = "(.*)"', init_py).groups()[0]

# obtain long description from README and CHANGES
try:
    # obtain long description from README and CHANGES
    with io.open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
        README = f.read()
        idx = README.index('<table border="0">')
        README = README[:idx]

except IOError:
    README = CHANGES = ''

# setup
setup(
    name='brainpy-simulator',
    version=version,
    description='BrainPy: A general platform for computational neuroscience and brain-inspired computation',
    long_description=README,
    author='Chaoming Wang',
    author_email='adaduo@outlook.com',
    packages=find_packages(exclude=['examples*', 'docs*', 'develop*', 'tests*']),
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.15',
        'matplotlib>=3.2',
    ],
    url='https://github.com/PKU-NIP-Lab/BrainPy',
    keywords='computational neuroscience, '
             'brain-inspired computation, '
             'dynamical systems, '
             'differential equations, '
             'numerical integration, '
             'ordinary differential equations, '
             'stochastic differential equations, '
             'delay differential equations, '
             'fractional differential equations, '
             'ODE, SDE, DDE, FDE',
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
    ]
)
