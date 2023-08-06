import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.2'
PACKAGE_NAME = 'afrikpay_pip_sdk'
AUTHOR = 'Georges Ngandeu'
AUTHOR_EMAIL = 'georgesngandeu@gmail.com'
URL = 'https://github.com/Georges-Ngandeu/AfrikpayPythonSdk'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'A library to facilitate Afrikpay api integration'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
]

setup(name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    license=LICENSE,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)