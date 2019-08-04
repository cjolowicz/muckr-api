import setuptools


with open("README.md") as file:
    long_description = file.read()

with open("requirements/base.in") as file:
    install_requires = file.read().splitlines()

setuptools.setup(
    name="muckr-api",
    version="0.5.0",
    author="Claudio Jolowicz",
    author_email="mail@claudiojolowicz.com",
    description="muckr API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cjolowicz/muckr-api",
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
