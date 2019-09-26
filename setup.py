from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='flat_table',
    version='1.0.0',
    packages=find_packages(),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='A broader implementation of json_normalize()',
    author='Metin Senturk',
    author_email='metinsenturk@me.com',
    long_description=long_description,
    install_requires=[
        'pandas'
    ]
)
