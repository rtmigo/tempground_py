from pathlib import Path

from setuptools import setup, find_packages

name = "tempground"

setup(
    name=name,
    version="0.4.1",

    author="Artsiom iG",
    author_email="ortemeo@gmail.com",

    packages=find_packages(include=['tempground', 'tempground.*']),
    package_data={'tempground': ['py.typed']},

    python_requires='>=3.10',  # 3.10 for `match`
    install_requires=[],

    long_description=(Path(__file__).parent / 'README.md') \
        .read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',

    license="MIT",

    keywords="temp library unit testing integration".split(),

    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows"
    ],
)

