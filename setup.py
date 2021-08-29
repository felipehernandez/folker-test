"""Minimal setup file for tasks project."""
from pkg_resources import parse_requirements
from setuptools import setup

setup(
    name='folker',
    version='0.1.0',
    license='proprietary',
    description='Test and simple tasks automation tool',

    author='Felipe Hernandez',
    author_email='felherlla@gmail.com',
    url='https://github.com/felipehernandez/folker-test',

    packages=['folker'],
    
    install_reqs=parse_requirements('requirements.txt'),

    entry_points={
        'console_scripts': [
            'folker = folker.cli:run',
        ]
    },
)
