from setuptools import setup, find_namespace_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='ruiyi-koch-snowflake',
    version='0.0.2',
    author='Ruiyi',
    description="A koch snowflake interactive app",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://altitude.otago.ac.nz/rqian/cosc326-koch-snowflake-interactive.git",
    packages=find_namespace_packages(include=["src", "src.*"]),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'snowflake = src.app:main',
        ],
    },
)
