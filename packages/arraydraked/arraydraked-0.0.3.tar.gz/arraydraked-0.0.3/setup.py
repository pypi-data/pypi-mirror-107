from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.3'
DESCRIPTION = 'An array duplicate checker'
LONG_DESCRIPTION = './README.md'

# Setting up
setup(
    name="arraydraked",
    version=VERSION,
    author="Aswin Sankar",
    author_email="<AswinSankar18@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['array','duplicate'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)