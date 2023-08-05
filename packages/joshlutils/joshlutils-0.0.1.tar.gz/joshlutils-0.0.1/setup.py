from setuptools import setup

VERSION = "0.0.1"
URL = "https://github.com/JoshLoecker/utils"
DOWNLOAD_URL = "https://github.com/JoshLoecker/utils/archive/refs/tags/0.0.1.tar.gz"

with open("README.md", "r") as i_stream:
    LONG_DESCRIPTION = i_stream.read()

setup(
    name='joshlutils',
    packages=['joshlutils'],
    version=VERSION,
    description='A simple utility package for various tasks I commonly perform',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author='Josh Loecker',
    author_email='joshloecker@icloud.com',
    url=URL,
    download_url=DOWNLOAD_URL,
    keywords=["Python", "Python 3", "Email"],
    classifiers=[],
)
