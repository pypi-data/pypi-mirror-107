from setuptools import setup
from os.path import join, dirname

setup(
    name='unique_variable',
    version='1.0',
    packages=['unique_variable'],
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author_email='dimapyatetsky@gmail.com'
    )
