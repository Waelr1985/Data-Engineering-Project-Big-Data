from setuptools import setup, find_packages

setup(
    name="skin",
    version="0.1",
    packages=find_packages(where="."),  # '.' specifies that packages are in the current directory structure
    install_requires=[]  # Include any dependencies if needed
)
