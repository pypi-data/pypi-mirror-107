from setuptools import setup,find_namespace_packages,find_packages
import os
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='VetstoriaNER',
install_requires=['spacy'],
setup_requires=['pytest-runner'],
tests_require=['pytest'],
python_requires='>=3.6.9',
version='0.7',
description='Species detection package for Vetstoria',
long_description=long_description,
long_description_content_type='text/markdown',
classifiers=['Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python'],            
author='Vetstoria',
author_email='riza@vetstoria.com',
packages=find_packages(include=['VetstoriaNER','ner_tests']),
zip_safe=False)