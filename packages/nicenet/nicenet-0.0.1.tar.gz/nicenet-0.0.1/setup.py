#!/usr/bin/python3

from setuptools import setup, find_packages

with open("README.md", 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    install_requires = fh.read().splitlines()


print(find_packages())

setup(
    name='nicenet',
    version='0.0.1',
    author="Subhash Sarangi",
    author_email="subhashsarangi123@gmail.com",
    url="https://github.com/Subhash3/Neural_Net_Using_NumPy/",
    packages=find_packages(),
    description='Feed Forward Neural Networks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    # py_modules=["shineflow"],
    # package_dir={'': 'shineflow'},
    install_requires=install_requires,
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        #"License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
)
