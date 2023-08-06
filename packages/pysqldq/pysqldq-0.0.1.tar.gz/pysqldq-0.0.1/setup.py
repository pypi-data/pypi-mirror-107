from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()
    


setup(
    name="pysqldq",
    version="0.0.1",
    author="Akshay Katre",
    author_email="akshaykatre@gmail.com",
    description="A library to create dynamic SQL data quality checks",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pysqldq-project/pysqldq/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
)
