from setuptools import setup, find_packages

setup(
    name='flat_table',
    version='1.0.0',
    packages=find_packages(),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='A broader implementation of json_normalize()',
    author='Metin Senturk',
    author_email='metinsenturk@me.com',
    long_description=open('README.md').read(),
    install_requires=[
        'pandas'
    ]
)