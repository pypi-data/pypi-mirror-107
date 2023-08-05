from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = 'splaxa',
    version = '1.0',
    url = 'https://github.com/NfrXDRA',
    download_url = 'https://github.com/NeforMan/AminoN/tree/master',
    license = 'MIT',
    author = 'NfrXDRA',
    author_email = 'email@gmail.com',
    description = 'A library to create Amino bots.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    keywords = [
        'aminoapps',
        'amino-py',
        'amino',
        'amino-bot',
        'narvii',
        'api',
        'python',
        'python3',
        'python3.x',
        'slimakoi',
        'official'
    ],
    install_requires = [
        'requests'
    ],
    setup_requires = [
        'wheel'
    ],
    packages = find_packages()
)