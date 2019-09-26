from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='flat_table',
    version='1.0.0',
    packages=['flat_table'],
    license='MIT',
    author='Metin Senturk',
    author_email='metinsenturk@me.com',
    url='https://github.com/metinsenturk/flat_table',
    keywords=['pandas', 'json_normalize', 'dict_to_columns', 'flatten'],
    description='A broader implementation of pandas json_normalize function.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'pandas'
    ],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ],
)
