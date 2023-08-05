import codecs
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'Django Ninja package to integrate keycloak authentication'
LONG_DESCRIPTION = 'A package that allows to build keycloak based authentication.'

# Setting up
setup(
    name="django-ninja-keycloak",
    version=VERSION,
    author="kgaulin (Kevin Gaulin)",
    description=DESCRIPTION,
    packages=['django-ninja-keycloak'],
    install_requires=['python-keycloak', 'django-ninja', 'pyjwt'],
    keywords=['python', 'django-ninja', 'keycloak'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)