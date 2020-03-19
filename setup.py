from os.path import join, dirname

from setuptools import setup, find_packages

setup(
    name='pyrapid',
    version='0.0.1',
    packages=find_packages(exclude=['venv', '.gitignore', '.git']),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    author='Exactor96',
    author_email='kyzya96@gmail.com',
    url='https://github.com/Exactor96/pyrapid',
    install_requires=open(join(dirname(__file__), 'requirements.txt')).read()
)
