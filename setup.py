from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='flat_table',
    version='1.0.0',
    packages=find_packages(),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='A broader implementation of json_normalize()',
    author='Metin Senturk',
    author_email='metinsenturk@me.com',
    url='https://github.com/metinsenturk/flat_table'
    keywords=['pandas', 'json_normalize', 'dict_to_columns', 'flatten']
    long_description=long_description,
    install_requires=[
        'pandas'
    ]
)
