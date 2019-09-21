# Contributor Guide

- [Environment](#environment)
- [Code Style](#code-style)
- [Testing](#testing)
- [Development Server](#development-server)
- [Continuous Integration](#continuous-integration)
- [Deployment](#deployment)
- [Releasing](#releasing)

## Environment

You need Python 3.7 and the following tools:

- [poetry](https://poetry.eustace.io/)
- [nox](https://nox.thea.codes/)
- [pyenv](https://github.com/pyenv/pyenv) (optional)

Install the package with development requirements:

```sh
$ poetry install
```

## Code Style

Reformat your changes before committing:

```sh
$ nox -e black
```

## Testing

The test suite is located under [tests](tests) and uses
[pytest](https://pypi.org/project/pytest/).

Run the test suite as follows:

```sh
$ nox
```

## Development Server

First, configure the app as described in [Configuration](README.md#configuration).

Start up the database server:

```sh
$ docker-compose -f docker-compose.dev.yml up
```

Run the database migrations:

```sh
$ muckr-api db upgrade
```

Start up the API in development mode:

```sh
$ muckr-api run
```

Point your browser to http://localhost:5000/.

## Continuous Integration

Continuous integration is provided by
[Travis CI](https://travis-ci.org). The Travis CI job runs the test
suite.

## Deployment

The app is deployed to a [Heroku](https://heroku.com) pipeline. Deployment to
staging happens automatically on every change to `master` that passes CI.
Deployment to production is done manually through the Heroku dashboard.

- https://muckr-api-staging.herokuapp.com/
- https://muckr-api.herokuapp.com/

Review apps are created automatically for Pull Requests using the
[app.json](app.json) configuration file.

To migrate the production database on Heroku,

```sh
$ heroku run muckr-api db upgrade --app=muckr-api
```

(Use `--app=muckr-api-staging` to migrate the staging database.)

## Releasing

This project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) and
[PEP 440](https://www.python.org/dev/peps/pep-0440).

1. Update [CHANGELOG.md](CHANGELOG.md).
2. Bump version using `poetry version`.
3. Update the version number in `__init__.py`.
4. Add a Git tag to the repository.
5. Push to Github.
6. Create the Github release.

Useful scripts to help with the above:

- https://github.com/cjolowicz/scripts/blob/master/github/bumpversion-changelog.sh
- https://github.com/cjolowicz/scripts/blob/master/github/bumpversion-poetry.sh
- https://github.com/cjolowicz/scripts/blob/master/github/github-release.sh

Example shell session:

```sh
$ bumpversion-changelog 0.6.0
$ bumpversion-poetry --push 0.6.0
$ github-release 0.6.0
```

Steps to be done after release:

1. Wait for CI.
2. Wait for deployment to staging.
3. If all looks good, promote staging to production.
