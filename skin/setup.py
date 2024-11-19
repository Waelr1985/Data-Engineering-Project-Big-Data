from setuptools import setup, find_packages

setup(
    name="skin",
    version="0.0.0",
    author="wael",
    author_email="waelr1985@gmail.com",
    packages=find_packages()
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "numpy",
        "pandas",
        "pyspark"
)