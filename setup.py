from setuptools import setup, find_packages

setup(
    name='sciencedirectFlatFileParse',
    version='1.0.0',
    description='A parser for ScienceDirect Flat File XML files',
    author='DaaS_CSC',
    author_email='',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'lxml'
    ],
    python_requires='>=3.10',
)