from setuptools import setup, find_packages

setup(
    name="data_ingestion",
    version="0.1",
    packages=find_packages(include=["skin", "skin.*"]),
    install_requires=[
        # Any specific dependencies for this microservice
    ],
)
