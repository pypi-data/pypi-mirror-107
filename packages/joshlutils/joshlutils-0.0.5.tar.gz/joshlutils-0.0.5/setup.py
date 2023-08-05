from setuptools import setup, find_packages

VERSION = "0.0.5"
URL = "https://github.com/JoshLoecker/utils"
DOWNLOAD_URL = f"https://github.com/JoshLoecker/utils/archive/refs/tags/{VERSION}.tar.gz"

with open("README.md", "r") as i_stream:
    LONG_DESCRIPTION = i_stream.read()

setup(
    name='joshlutils',
    packages=find_packages(),
    version=VERSION,
    install_requires=[
        "keyring",
        "smtplib",
        "email",
        "imap_tools"
    ],
    description='A simple utility package for various tasks I commonly perform',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author='Josh Loecker',
    author_email='joshloecker@icloud.com',
    url=URL,
    download_url=DOWNLOAD_URL,
    keywords=["Python", "Python 3", "Email"],
    license="MIT",
    classifiers=[],
)
