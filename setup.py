import setuptools


with open("VERSION") as file:
    version = file.read()

with open("README.md") as file:
    long_description = file.read()

with open("requirements/base.in") as file:
    install_requires = file.read().splitlines()

setuptools.setup(
    name="muckr-service",
    version=version,
    author="Claudio Jolowicz",
    author_email="mail@claudiojolowicz.com",
    description="Web service for muckr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cjolowicz/muckr-service",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
    ],
)
