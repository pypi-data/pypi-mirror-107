from setuptools import setup, find_packages
import pathlib


# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name='npaws',
    packages=find_packages(),
    description='An SDK that provides functionalities for Neural Platform Project.',
    long_description=README,
    version='0.1.0',
    url='https://github.com/miquelescobar/npaws',
    author='Miquel Escobar',
    author_email='miquel.escobar@bsc.es',
    keywords=['pip','neural','platform','npaws']
)