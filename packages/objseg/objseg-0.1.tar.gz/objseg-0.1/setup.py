# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:43:42 2020

@author: hinsm
"""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="objseg", # Replace with your own username
    version="0.1",
    author="Jenkin Tsui",
    author_email="jenkin.tsui@aya.yale.edu",
    description="A cell segmentation pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tsuijenk/BLMPP",
    packages=find_packages(),
    include_package_data=True,
    license='GPL v3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    py_modules=['cli'],
    install_requires=[
	'click', 'h5py', 'Pandas', 'Pillow', 'datetime', 'numpy', 'numba', 'scipy', 'matplotlib', 'sklearn', 'opencv_python', 'rtree'
	],
    entry_points={
        'console_scripts':[
            'objseg = objseg.cli:main',
        ]
    }
)