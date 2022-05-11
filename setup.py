"""Minimal setup file for tasks project."""
from setuptools import setup

setup(
    name='folker-test',
    version='2.3',
    license='proprietary',
    description='Test and simple tasks automation tool',

    author='Felipe Hernandez',
    author_email='felherlla@gmail.com',
    url='https://github.com/felipehernandez/folker-test',

    packages=['folker'],

    install_requires=[
        'certifi==2020.4.5.1',
        'chardet==4.0.0',
        'click==7.1.2',
        'coverage',
        'google==3.0.0',
        'google-api-python-client==1.12.11',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'google-cloud-pubsub==1.7.1',
        'google-cloud-datastore==2.4.0',
        'gql==2.0.0',
        'grpcio==1.45.0',
        'grpcio-tools==1.43.0',
        'httplib2==0.20.4',
        'idna==2.10',
        'kafka-python==2.0.2',
        'kazoo==2.8.0',
        'marshmallow==3.14.1',
        'marshmallow-oneofschema==3.0.1',
        'mergedeep==1.3.4',
        'oauth2client==4.1.3',
        'pika==1.2.1',
        'psycopg2-binary==2.9.3',
        'pylint==2.13.8',
        'pyOpenSSL==22.0.0',
        'PyYAML==6.0',
        'requests==2.27.1',
    ],

    entry_points={
        'console_scripts': [
            'folker-test = folker.cli:run',
        ]
    },
)
