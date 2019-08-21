# Contributing

- [Development](#development)
- [Testing](#testing)
- [Running](#running)
- [Requirements](#requirements)
- [Releasing](#releasing)
- [Continuous Integration](#continuous-integration)
- [Deployment](#deployment)

## Development

You need Python 3.7 and the following tools:

- [poetry](https://poetry.eustace.io/)
- [nox](https://nox.thea.codes/)
- [pyenv](https://github.com/pyenv/pyenv) (optional)

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

The following command will start up the API:

```sh
docker-compose up
```

The Docker Compose file comprises the following Docker containers:

- `muckr-api`
- `muckr-api-nginx`
- `postgres`
- `adminer`

Database files are stored on a volume named `database`.

The API is accessible on port 9000 on the Docker host. The database management
interface is accessible on port 9001 on the Docker host.

Use the following command to create the admin user:

```sh
docker-compose exec muckr-api flask create-admin
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

## Deployment

The app is deployed to a [Heroku](https://heroku.com) pipeline. Deployment to
staging happens automatically on every change to `master` that passes CI.
Deployment to production is done manually through the Heroku dashboard.

- https://muckr-api-staging.herokuapp.com/
- https://muckr-api.herokuapp.com/

Review apps are created automatically for Pull Requests using the
[app.json](app.json) configuration file.

To migrate the database on Heroku,

```sh
heroku run --app=muckr-api-staging flask db upgrade
```

(Use `--app=muckr-api` to migrate the production database.)
