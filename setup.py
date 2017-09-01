
import os.path

from setuptools import setup, find_packages


__version__ = 'devel'

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


requires = [
    'flask',
]

setup(
    name='pybowieconsole',
    version=__version__,
    description='Web console for Bowie',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
    ],
    author='David Kavanagh',
    author_email='dkavanagh@gmail.com',
    url='',
    keywords='',
    packages=find_packages(),
    install_requires=requires
)
