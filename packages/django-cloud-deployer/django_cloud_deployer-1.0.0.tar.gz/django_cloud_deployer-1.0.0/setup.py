import setuptools
from os import path

dir = path.abspath(path.dirname(__file__))
with open(path.join(dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="django_cloud_deployer",
    version="1.0.0",
    author="Rui Alves",
    description="Hybrid cloud deployment (IaaS/PaaS and FaaS) of Django web applications.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[
        'asgiref>=3.3.4',
        'azf-wsgi>=0.3.1',
        'azure-functions>=1.7.0',
        'azure-functions-worker>=1.1.9',
        'chevron>=0.14.0',
        'Django>=3.1.7',
        'grpcio>=1.33.2',
        'grpcio-tools>=1.33.2',
        'protobuf>=3.16.0',
        'pytz>=2021.1',
        'six>=1.16.0',
        'sqlparse>=0.4.1',
        'termcolor>=1.1.0',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    package_data={'': ['config_files/**/*']},
)
