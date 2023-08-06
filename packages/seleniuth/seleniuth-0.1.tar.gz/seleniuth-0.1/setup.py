import setuptools
from setuptools import version

setuptools.setup(
    name="seleniuth",
    version="0.1",
    license="MIT",
    author="ros4s",
    author_email="c01066033993@gmail.com",
    description="Selenium Web Login",
    long_description=open('README.md').read(),
    url="https://github.com/ros4s/seleniuth",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)