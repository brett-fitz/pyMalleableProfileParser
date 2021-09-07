from setuptools import setup, find_packages

from mpp import __author__, __version__, __license__

try:
    with open("README.md", encoding="utf8") as readme_file:
        readme = readme_file.read()
except TypeError:
    with open("README.md") as readme_file:
        readme = readme_file.read()

setup(
    name="pyMalleableProfileParser",
    author=__author__,
    version=__version__,
    license=__license__,
    description="Parses Cobalt Strike malleable C2 profiles",
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/brett-fitz/pyMalleableProfileParser',
    keywords=['cobalt strike', 'malleable profile', 'parser'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='~=3.5',
    packages=find_packages()
)
