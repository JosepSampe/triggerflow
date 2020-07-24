from setuptools import setup, find_packages

setup(
    name='triggerflow',
    version='0.2.0',
    url='https://github.com/triggerflow',
    author='Triggerflow Team',
    description='Event-based Orchestration of Serverless Workflows',
    author_email='cloudlab@urv.cat',
    packages=find_packages(),
    install_requires=[
        'gevent',
        'pika==0.13.1',
        'flask',
        'PyYAML',
        'confluent-kafka',
        'dill',
        'jsonpath_ng',
        'requests',
        'python-dateutil',
        'docker',
        'redis>=3.5.3',
        'boto3',
        'click',
        'graphviz',
        'arnparse',
        'dataclasses',
        'kubernetes',
        'cloudpickle'
    ],
    include_package_data=True,
    entry_points='''
        [console_scripts]
        triggerflow=triggerflow.cli.cli:entry_point
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
