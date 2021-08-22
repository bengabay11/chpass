import setuptools
from chpass.version import (
    name,
    version,
    author,
    author_email,
    license,
    description,
    url
)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    license=license,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    packages=setuptools.find_packages(),
    install_requires=[
        "sqlalchemy==1.3.18",
        "pandas==1.3.1",
        "pattern_singleton==1.2.0"
    ],
    python_requires=">=3",
    entry_points={
        'console_scripts': ['chpass = chpass.__init__:main'],
    },
    keywords="chrome passwords",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
