from os.path import join, dirname

from setuptools import setup, find_packages

setup(
    name='pyrapid',
    version='0.0.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=open(join(dirname(__file__), 'requirements.txt')).read()
)
