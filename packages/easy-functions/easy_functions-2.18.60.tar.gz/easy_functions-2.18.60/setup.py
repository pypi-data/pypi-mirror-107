from setuptools import setup
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name = 'easy_functions',
    version = '2.18.60',
    py_modules = ['easy_functions'],
    author = 'Jerry0940',
    author_email = 'j13816180940@139.com',
    license = 'MIT',
    description = '一个简单小巧但实用的模块',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    classifiers = [
        "Programming Language :: Python :: 3"
    ]
)