import os
import sys
import shutil
from setuptools import setup, find_packages, Extension

setup(
    name="pylibxc2",
    version="0.0.1",
    description='Pylibxc',
    url='https://github.com/mfkasim1/pylibxc/',
    author='mfkasim1',
    author_email='firman.kasim@gmail.com',
    license='Apache License 2.0',
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.8.2",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="project library dft quantum-chemistry",
    zip_safe=False
)
