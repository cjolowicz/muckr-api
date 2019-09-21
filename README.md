[![Build Status](https://img.shields.io/travis/cjolowicz/muckr-api.svg?style=flat-square)](https://travis-ci.org/cjolowicz/muckr-api)
[![Coverage Status](https://img.shields.io/coveralls/cjolowicz/muckr-api.svg?style=flat-square)](https://coveralls.io/github/cjolowicz/muckr-api?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

# muckr-api

muckr API

- [Contents](#contents)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running](#running)

## Contents

This package defines an API using the [Flask](http://flask.pocoo.org/)
microframework.

| Module                                                  | Description                                  |
| ---                                                     | ---                                          |
| [`muckr_api.app`](muckr_api/app.py)                     | Defines the app                              |
| [`muckr_api.extensions`](muckr_api/extensions.py)       | Flask extensions                             |
| [`muckr_api.config`](muckr_api/config.py)               | Reads the configuration from the environment |
| [`muckr_api.errors`](muckr_api/errors.py)               | Implements error handling                    |
| [`muckr_api.user.models`](muckr_api/user/models.py)     | Defines the user model                       |
| [`muckr_api.user.auth`](muckr_api/user/auth.py)         | Implements user authentication               |
| [`muckr_api.user.views`](muckr_api/user/views.py)       | Implements the user-related views            |
| [`muckr_api.main.views`](muckr_api/main/views.py)       | Defines the main views (placeholder)         |
| [`muckr_api.artist.models`](muckr_api/artist/models.py) | Defines the artist model                     |
| [`muckr_api.artist.views`](muckr_api/artist/views.py)   | Implements the artist-related views          |
| [`muckr_api.venue.models`](muckr_api/venue/models.py)   | Defines the venue model                      |
| [`muckr_api.venue.views`](muckr_api/venue/views.py)     | Implements the venue-related views           |

## Installation

To install this package, clone the repository and run the following command at
the top-level directory:

```sh
pip install .
```

## Configuration

The app is configured via the following environment variables:

| Environment Variable | Default           |
| ---                  | ---               |
| `ADMIN_EMAIL`        | `admin@localhost` |
| `ADMIN_PASSWORD`     | *required*        |
| `ADMIN_USERNAME`     | `admin`           |
| `BCRYPT_LOG_ROUNDS`  | 12                |
| `DATABASE_URL`       | *required*        |
| `SECRET_KEY`         | *required*        |

The database server is configured via the following environment variables:

| Environment Variable | Default    |
| ---                  | ---        |
| `POSTGRES_USER`      | `postgres` |
| `POSTGRES_PASSWORD`  | *required* |
| `POSTGRES_DB`        | `postgres` |

A sample [env file](.env.sample) is provided. This is a file named
`.env`, where each line contains an assignment of the form `VAR=VAL`.

### Running

The following command will start up the API:

```sh
$ docker-compose up
```

The Docker Compose file comprises the following Docker containers:

| Container         | Image                                                                                                                                 | Description                      |
| ---               | ---                                                                                                                                   | ---                              |
| `muckr-api`       | [Dockerfile](Dockerfile)                                                                                                              | the API itself                   |
| `muckr-api-nginx` | [nginx/Dockerfile](nginx/Dockerfile)                                                                                                  | an nginx proxy for the API       |
| `postgres`        | [postgres:11.2-alpine](https://github.com/docker-library/postgres/blob/6c3b27f1433ad81675afb386a182098dc867e3e8/11/alpine/Dockerfile) | the database server              |
| `adminer`         | [adminer](https://github.com/TimWolla/docker-adminer/blob/0b7ac63344767be6d7903444f40d8b9885b5d7bd/4/Dockerfile)                      | a web interface for the database |

Database files are stored on a volume named `muckr-api_database`.

The API is accessible on port `9000` on the Docker host. The database management
interface is accessible on port `9001` on the Docker host.

Use the following command to create the admin user:

```sh
$ docker-compose exec muckr-api muckr-api create-admin
```
