from setuptools import setup, find_packages

setup(
    name='dmsales',
    version='0.1.7',
    description='DMSales API Python Client',
    packages=find_packages(),
    install_requires=[
        'requests==2.25.1',
        'typing-extensions==3.10.0.0'
    ]
)