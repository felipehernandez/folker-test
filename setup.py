"""Minimal setup file for tasks project."""
from setuptools import setup

setup(
    name='folker-test',
    version='2.5',
    license='proprietary',
    description='Test and simple tasks automation tool',

    author='Felipe Hernandez',
    author_email='felherlla@gmail.com',
    url='https://github.com/felipehernandez/folker-test',

    packages=['folker'],

    install_requires=[
        'certifi==2023.11.17',
        'chardet==5.2.0',
        'click==8.1.7',
        'coverage',
        'google==3.0.0',
        'google-api-python-client==2.139.0',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'google-cloud-pubsub==1.7.2',
        'gql==2.0.0',
        'grpcio==1.65.4',
        'grpcio-tools==1.48.1',
        'httplib2==0.22.0',
        'idna==3.7',
        'kafka-python==2.0.2',
        'kazoo==2.10.0',
        'marshmallow==3.21.3',
        'marshmallow-oneofschema==3.1.1',
        'mergedeep==1.3.4',
        'oauth2client==4.1.3',
        'pika==1.3.2',
        'psycopg2-binary==2.9.9',
        'pylint==3.2.6',
        'pyOpenSSL==23.3.0',
        'PyYAML==6.0.1',
        'requests==2.32.3',
    ],

    entry_points={
        'console_scripts': [
            'folker-test = folker.cli:run',
        ]
    },
)
