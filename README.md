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
