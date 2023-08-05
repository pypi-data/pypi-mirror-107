import setuptools

"""
:authors: Lexinus
:license: Apache License, version 2.0, see LICENSE file
:copyright: (c) 2021 Lexinus
"""

version = '0.1.1'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="steganography_in_text",
    version=version,
    author="Lexinus",
    license='Apache License, version 2.0, see LICENSE file',
    author_email="starshenkov3@gmail.com",
    description="Это модуль, умеющий скрывать текст в тексте",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/red-lexinus/steganography_in_text",
    project_urls={
        "Bug Tracker": "https://github.com/red-lexinus/steganography_in_text",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={},
    packages=['steganography_in_text'],
    python_requires=">=3.6",
)
