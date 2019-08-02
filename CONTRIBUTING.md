# Contributing

- [Development](#development)
- [Testing](#testing)
- [Running](#running)
- [Requirements](#requirements)
- [Releasing](#releasing)
- [Continuous Integration](#continuous-integration)

## Development

First, make sure you have `python3.7` in your `PATH`.

```sh
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
pyenv install 3.7.1
pyenv local 3.7.1
```

Reformat your changes before committing:

```sh
nox -e black
```

## Testing

The test suite is located under [tests](tests) and uses
[pytest](https://pypi.org/project/pytest/).

Run the test suite as follows:

```sh
nox
```

## Running

The following command will start up the web service:

```sh
docker-compose up
```

The Docker Compose file comprises the following Docker containers:

- `muckr-service`
- `muckr-service-nginx`
- `postgres`
- `adminer`

Database files are stored on a volume named `database`.

The web service is accessible on port 9000 on the Docker host. The database
management interface is accessible on port 8080 on the Docker host.

Use the following command to create the admin user:

```sh
docker-compose exec muckr-service flask create-admin
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
nox -e upgrade
```

## Releasing

This project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) and
[PEP 440](https://www.python.org/dev/peps/pep-0440).

The [bumpversion](https://pypi.org/project/bumpversion/) tool is used
to update the version number and add a Git tag to the repository.

1. Run `nox`.
2. Update [CHANGELOG.md](CHANGELOG.md).
3. Bump version.
4. Push to Github.

## Continuous Integration

Continuous integration is provided by
[Travis CI](https://travis-ci.org). The Travis CI job runs the test
suite.
