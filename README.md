[![Build Status](https://img.shields.io/travis/cjolowicz/muckr-api.svg?style=flat-square)](https://travis-ci.org/cjolowicz/muckr-api)
[![Coverage Status](https://img.shields.io/coveralls/cjolowicz/muckr-api.svg?style=flat-square)](https://coveralls.io/github/cjolowicz/muckr-api?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

# muckr-api

muckr API

- [Contents](#contents)
- [Installation](#installation)
- [Configuration](#configuration)

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

Also, use these environment variables for Flask:

| Environment Variable | Default       |
| ---                  | ---           |
| `FLASK_APP`          | `wsgi.py`     |
| `FLASK_ENV`          | `development` |

A sample [env file](.env.sample) is provided. This is a file named
`.env`, where each line contains an assignment of the form `VAR=VAL`.
