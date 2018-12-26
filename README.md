[![Build Status](https://img.shields.io/travis/cjolowicz/muckr-service.svg?style=flat-square)](https://travis-ci.org/cjolowicz/muckr-service)
[![Coverage Status](https://img.shields.io/coveralls/cjolowicz/muckr-service.svg?style=flat-square)](https://coveralls.io/github/cjolowicz/muckr-service?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

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
- The artist model is defined in
  [muckr.artist.models](muckr/artist/models.py).
- The artist-related views are implemented in
  [muckr.artist.views](muckr/artist/views.py).

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

Reformat your changes before committing:

```sh
make black
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

- `ADMIN_EMAIL` (default: `admin@localhost`)
- `ADMIN_PASSWORD` (required)
- `ADMIN_USERNAME` (default: `admin`)
- `BCRYPT_LOG_ROUNDS` (default: 12)
- `DATABASE_URL` (required)
- `SECRET_KEY` (required)

The database server is configured via the following environment variables:

- `POSTGRES_USER` (default: `postgres`)
- `POSTGRES_PASSWORD` (required)
- `POSTGRES_DB` (default: `postgres`)

Also, use these environment variables for Flask:

- `FLASK_APP=wsgi.py`
- `FLASK_ENV=development`

A sample [env file](.env.sample) is provided. This is a file named
`.env`, where each line contains an assignment of the form `VAR=VAL`.

## Running

To start up the database server:

```sh
docker swarm init
docker stack deploy -c postgres.yml postgres
flask db upgrade
flask create-admin
```

To start up a development instance of the web server:

```sh
flask run
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

This project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) and
[PEP 440](https://www.python.org/dev/peps/pep-0440).

The [bumpversion](https://pypi.org/project/bumpversion/) tool is used
to update the version number and add a Git tag to the repository.

1. Run `make test`.
2. Update [CHANGELOG.md](CHANGELOG.md).
3. Bump version.
4. Push to Github.

## Continuous Integration

Continuous integration is provided by
[Travis CI](https://travis-ci.org). The Travis CI job runs the test
suite.

## Deployment

The app is deployed to [Heroku](https://heroku.com) automatically on
every change to `master` that passes CI.

- https://muckr-service.herokuapp.com/

To generate the secrets for Heroku,

```sh
make heroku-secretkey heroku-adminpassword
```

To migrate the database on Heroku,

```sh
make heroku-db-upgrade
```
