[![Build Status](https://img.shields.io/travis/cjolowicz/muckr-service.svg?style=flat-square)](https://travis-ci.org/cjolowicz/muckr-service)
[![Coverage Status](https://img.shields.io/coveralls/cjolowicz/muckr-service.svg?style=flat-square)](https://coveralls.io/github/cjolowicz/muckr-service?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

# muckr-service

Web service for muckr

This project has a [changelog](CHANGELOG.md).

- [Contents](#contents)
- [Installation](#installation)
- [Configuration](#configuration)
- [Deployment](#deployment)

## Contents

This package defines a web service using the
[Flask](http://flask.pocoo.org/) microframework.

| Module                                        | Description                                  |
| ---                                           | ---                                          |
| [muckr.app](muckr/app.py)                     | Defines the app                              |
| [muckr.extensions](muckr/extensions.py)       | Flask extensions                             |
| [muckr.config](muckr/config.py)               | Reads the configuration from the environment |
| [muckr.errors](muckr/errors.py)               | Implements error handling                    |
| [muckr.user.models](muckr/user/models.py)     | Defines the user model                       |
| [muckr.user.auth](muckr/user/auth.py)         | Implements user authentication               |
| [muckr.user.views](muckr/user/views.py)       | Implements the user-related views            |
| [muckr.main.views](muckr/main/views.py)       | Defines the main views (placeholder)         |
| [muckr.artist.models](muckr/artist/models.py) | Defines the artist model                     |
| [muckr.artist.views](muckr/artist/views.py)   | Implements the artist-related views          |
| [muckr.venue.models](muckr/venue/models.py)   | Defines the venue model                      |
| [muckr.venue.views](muckr/venue/views.py)     | Implements the venue-related views           |

## Installation

To install this package,

```sh
pip install muckr-service
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

Also, use these environment variables for Flask:

| Environment Variable | Default       |
| ---                  | ---           |
| `FLASK_APP`          | `wsgi.py`     |
| `FLASK_ENV`          | `development` |

A sample [env file](.env.sample) is provided. This is a file named
`.env`, where each line contains an assignment of the form `VAR=VAL`.

## Deployment

The app is deployed to [Heroku](https://heroku.com) automatically on
every change to `master` that passes CI.

- https://muckr-service.herokuapp.com/

To generate the secrets for Heroku,

```sh
heroku config:set --app=muckr-service SECRET_KEY=xxxxxx
heroku config:set --app=muckr-service ADMIN_PASSWORD=xxxxxx
```

To migrate the database on Heroku,

```sh
heroku run --app=muckr-service flask db upgrade
```
