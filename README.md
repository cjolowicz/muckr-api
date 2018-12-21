[![Build Status](https://travis-ci.org/cjolowicz/muckr-service.svg?branch=master)](https://travis-ci.org/cjolowicz/muckr-service)

# muckr-service

Web service for muckr

- [Installation](#installation)
- [Contents](#contents)
- [Development](#development)
- [Testing](#testing)
- [Running](#running)
- [Requirements](#requirements)
- [Continous Integration](#continous-integration)
- [Deployment](#deployment)

## Installation

To install this package,

```sh
pip install muckr-service
```

## Contents

This package defines a web service using the
[Flask](http://flask.pocoo.org/) microframework.

- The app factory function is [muckr.app.create_app](muckr/app.py).
- Flask extensions are in [muckr.extensions](muckr/extensions.py).
- The application configuration is read from the environment, in
  [muckr.config](muckr/config.py).
- Error handling is implemented in [muckr.errors](muckr/errors.py).
- The User model is defined in
  [muckr.user.models](muckr/user/models.py).
- User authentication s implemented in
  [muckr.user.auth](muckr/user/auth.py).
- The user-related views are implemented in
  [muckr.user.views](muckr/user/views.py).
- The main views are defined in
  [muckr.main.views](muckr/main/views.py). This is currently a
  placeholder.

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

## Continuous Integration

Continous integration is provided by
[Travis CI](https://travis-ci.org). The Travis CI job runs the test
suite.

## Deployment

The app is deployed to [Heroku](https://heroku.com) automatically on
every change to `master` that passes CI.

- https://muckr-service.herokuapp.com/
