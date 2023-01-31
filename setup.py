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
        'certifi==2022.12.7',
        'chardet==5.1.0',
        'click==8.1.3',
        'coverage',
        'google==3.0.0',
        'google-api-python-client==2.75.0',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'google-cloud-pubsub==1.7.2',
        'google-cloud-datastore==2.13.2',
        'gql==2.0.0',
        'grpcio==1.51.1',
        'grpcio-tools==1.48.1',
        'httplib2==0.21.0',
        'idna==3.4',
        'kafka-python==2.0.2',
        'kazoo==2.9.0',
        'marshmallow==3.19.0',
        'marshmallow-oneofschema==3.0.1',
        'mergedeep==1.3.4',
        'oauth2client==4.1.3',
        'pika==1.3.1',
        'psycopg2-binary==2.9.5',
        'pylint==2.15.10',
        'pyOpenSSL==23.0.0',
        'PyYAML==6.0',
        'requests==2.28.2',
    ],

    entry_points={
        'console_scripts': [
            'folker-test = folker.cli:run',
        ]
    },
)
