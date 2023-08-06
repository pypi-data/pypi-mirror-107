from setuptools import setup
import os.path

# The text of the README file
README = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Readme.md')).read()

# This call to setup() does all the work
setup(
    name="tbbackoff",
    version="0.0.4",
    description="Implementacion de token bucket con backoff exponencial",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/radiocutfm/tbbackoff",
    author="Lambda Sistemas",
    author_email="desarrollo@fierro.com.ar",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["tbbackoff"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)