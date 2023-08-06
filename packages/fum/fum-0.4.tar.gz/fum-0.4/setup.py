from setuptools import setup
import re

version_read = re.search(
    '^version\s*=\s*"(.*)"',
    open('fum/fum.py').read(),
    re.M
)

if version_read is not None:
    version = version_read.group(1)
else:
    version = "0.1"

print("version is " + version)

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
    long_description=long_descr
)
