from setuptools import setup
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('fum/fum.py').read(),
    re.M
).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name='fum',
    version=version,
    entry_points={
        "console_scripts": ['fum = fum.fum:main']
    },
    packages=['fum'],
    url='',
    license='',
    author='madhavth',
    author_email='',
    description='something not meant to be',
    long_descr=long_descr
)
