from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'This is a module that allows you to connect to the Comscore library developed by Annalect and obtain synthesized information'

# Setting up
setup(
    name="comscore_omg",
    version=VERSION,
    author="Data house CL",
    author_email="data.analitica@omnicommediagroup.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['sqlalchemy', 'pandas'],
    keywords=['python', 'omnicom', 'sql', 'comscore'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)