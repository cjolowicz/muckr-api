[![Build Status](https://img.shields.io/travis/cjolowicz/muckr-service.svg?style=flat-square)](https://travis-ci.org/cjolowicz/muckr-service)
[![Coverage Status](https://img.shields.io/coveralls/cjolowicz/muckr-service.svg?style=flat-square)](https://coveralls.io/github/cjolowicz/muckr-service?branch=master)

# muckr-service

Web service for muckr

This project has a [changelog](CHANGELOG.md).

- [Contents](#contents)
- [Installation](#installation)
- [Development](#development)
- [Testing](#testing)
- [Configuration](#configuration)
- [Running](#running)
- [Requirements](#requirements)
- [Releasing](#releasing)
- [Continuous Integration](#continuous-integration)
- [Deployment](#deployment)

## Contents

This package defines a web service using the
[Flask](http://flask.pocoo.org/) microframework.

- The app is defined in [muckr.app](muckr/app.py).
- Flask extensions are in [muckr.extensions](muckr/extensions.py).
- The configuration is read from the environment, in
  [muckr.config](muckr/config.py).
- Error handling is implemented in [muckr.errors](muckr/errors.py).
- The user model is defined in
  [muckr.user.models](muckr/user/models.py).
- User authentication is implemented in
  [muckr.user.auth](muckr/user/auth.py).
- The user-related views are implemented in
  [muckr.user.views](muckr/user/views.py).
- The main views are defined in
  [muckr.main.views](muckr/main/views.py). This is currently a
  placeholder.

## Installation

To install this package,

```sh
pip install muckr-service
```

## Development

First, make sure you have `python3.7` in your `PATH`.

```sh
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
pyenv install 3.7.1
pyenv local 3.7.1
```

Create a virtualenv and activate it:

```sh
make virtualenv
source venv/bin/activate
```

Install the development requirements as follows:

```sh
make install
```

## Testing

The test suite is located under [tests](tests) and uses
[pytest](https://pypi.org/project/pytest/).

Run the test suite as follows:

```sh
make test
```

## Configuration

The app is configured via the following environment variables:

- `DATABASE_URL`
- `SECRET_KEY`

Alternatively, provide an [env file](.env.sample). This is a file
named `.env`, where each line contains an assignment of the form
`VAR=VAL`.

## Running

To start up a development instance of the web server:

```shell
make flask-run
```

Alternatively, use `heroku local`:

```shell
make heroku-local
```

## Requirements

Requirements are declared in the files
[requirements/base.in](requirements/base.in) and
[requirements/dev.in](requirements/dev.in).

Requirements for production are pinned to specific versions in the
files [requirements/base.txt](requirements/base.txt) and
[requirements/dev.txt](requirements/dev.txt). These files are
generated using the following command:

```sh
make requirements
```

To force an upgrade of all requirements, invoke the following command:

```sh
make -B requirements
```

## Releasing

In the release workflow, every final release is preceded by a
development release.

### Making a development release

1. Run `make test`.
2. Update _Unreleased_ section in [CHANGELOG.md](CHANGELOG.md).
3. Bump version using `./bumpversion.sh [major|minor|patch|dev]`.
4. Push to Github.

### Making a final release

1. Run `make test`.
2. Rename _Unreleased_ section in [CHANGELOG.md](CHANGELOG.md).
3. Bump version using `./bumpversion.sh final`.
4. Push to Github.

### Bumping the version

This project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) and
[PEP 440](https://www.python.org/dev/peps/pep-0440).

The script [bumpversion.sh](bumpversion.sh) is used to update the
version number and add a Git tag to the repository.

- `./bumpversion.sh major` prepares a major release.
- `./bumpversion.sh minor` prepares a minor release.
- `./bumpversion.sh patch` prepares a patch release.

These will create development releases with a `.dev0` suffix.

- `./bumpversion.sh dev` creates another development release,
  by incrementing the `.devN` suffix.
- `./bumpversion.sh final` promotes a development release to a final
  release, by stripping off the `.devN` suffix.

## Continuous Integration

Continuous integration is provided by
[Travis CI](https://travis-ci.org). The Travis CI job runs the test
suite.

## Deployment

The app is deployed to [Heroku](https://heroku.com) automatically on
every change to `master` that passes CI.

- https://muckr-service.herokuapp.com/

To generate the secret key for Heroku,

```sh
make heroku-secretkey
```

To migrate the database on Heroku,

```sh
make heroku-db-upgrade
```
