from setuptools import setup, find_packages

with open('README.md') as file:
    long_description = file.read()

with open('requirements/base.in') as file:
    install_requires = file.read().splitlines()

with open('requirements/dev.in') as file:
    extras_require = {'dev': file.read().splitlines()}

setup(
    name='muckr-service',
    version='0.1.0',
    description='Web service for muckr',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    extras_require=extras_require,
)
