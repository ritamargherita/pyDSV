from setuptools import setup, find_packages

setup(
    name='pyDSV',
    version='0.1.0',
    description='A Python tool for converting CSV data into RDF using the DSV ontology',
    author='Margherita Martorana',
    author_email='m.martorana@vu.nl',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'rdflib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)