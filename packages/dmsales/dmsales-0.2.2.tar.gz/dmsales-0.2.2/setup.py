from setuptools import setup, find_packages

setup(
    name='dmsales',
    version='0.2.2',
    description='DMSales API Python Client',
    long_description='DMSales API Python Client',
    url='https://app.dmsales.com/api-doc/default',
    author='DMSales',
    author_email='data@dmsales.com',
    packages=find_packages(),
    install_requires=[
        'requests==2.25.1',
        'typing-extensions==3.10.0.0'
    ]
)
