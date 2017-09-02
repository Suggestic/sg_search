from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sg_search',
    version='0.0.1',
    description='Suggestic search',
    long_description=long_description,
    url='http://suggestic.com/',
    author='Ernesto V',
    author_email='ernesto@suggestic.com',
    license='MIT',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: SG Internal Devs',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='development',
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    py_modules=["sg_search"],
    install_requires=[
        'elasticsearch-dsl>=5.0.0,<6.0.0',
        'python-slugify==1.2.4'
    ],
    # $ pip install -e .[test]
    extras_require={
        'dev': ['coverage'],
    },

    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)
