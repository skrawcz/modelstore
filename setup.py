from setuptools import find_packages, setup

with open("README.md", "r") as lines:
    long_description = lines.read()

with open("requirements.txt", "r") as lines:
    requirements = lines.read().splitlines()

setup(
    name="modelstore",
    version="0.0.1b",
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    include_package_data=True,
    description="modelstore is a library for versioning, exporting, and storing machine learning models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/operatorai/modelstore",
    author="Neal Lathia",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
    ],
    license="Please refer to the readme",
    python_requires=">=3.6",
    install_requires=requirements,
)
