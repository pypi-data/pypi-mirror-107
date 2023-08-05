from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.5'
DESCRIPTION = 'A library for centering python gui windows.'
LONG_DESCRIPTION = 'A library that allows you to center python gui windows.'

# Setting up
setup(
    name="centerit",
    version=VERSION,
    author="Mrinmoy Haloi",
    author_email="<mhedeetz.business@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/MrinmoyHaloi/centerit",
    packages=find_packages(),
    keywords=['python', 'gui'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)