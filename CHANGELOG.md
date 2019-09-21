# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- Fix broken isolation of nox session when installing via Poetry ([#42](../../pull/42))
- Fix reverse migration for artist-user foreign key ([#45](../../pull/45))
- Fix invalid Heroku app name when retrieving client credentials ([#40](../../pull/40))

### Added
- Add integration tests ([#41](../../pull/41))

### Removed
- Drop bumpversion ([#38](../../pull/38))
- Drop adminer ([#43](../../pull/43))

### Changed
- Update documentation ([#39](../../pull/39))
- Improve client message when authentication fails ([#44](../../pull/44))
- Remove startup log message ([#46](../../pull/46))

## [0.6.0] - 2019-08-29
### Added
- Add commandline interface ([#32](../../pull/32))

### Changed
- Use [poetry](https://poetry.eustace.io/) build backend ([#34](../../pull/34))
- Use `localhost` in `DATABASE_URL`, except when using Docker Compose ([#35](../../pull/35))
- Do not copy .git directory into Docker images ([#36](../../pull/36))

## [0.5.0] - 2019-08-04
### Changed
- Rename project to muckr-api ([#30](../../pull/30))
- Rename package to muckr_api ([#31](../../pull/31))

## [0.4.2] - 2019-08-04
### Changed
- Documentation cleanup ([#23](../../pull/23))
- Move flake8 configuration to .flake8 ([#26](../../pull/26))
- Remove `VERSION` file ([#27](../../pull/27))
- Upgrade Heroku runtime to Python 3.7.3 ([#28](../../pull/28))

## [0.4.1] - 2019-08-03
### Fixed
- Fix broken Heroku deployment due to src layout ([#25](../../pull/25))

## [0.4.0] - 2019-08-03
### Added
- Add venues ([#19](../../pull/19)).
- Enable CI for pull requests ([#13](../../pull/13))
- Configure Heroku review apps using `app.json` ([#15](../../pull/15))
- Configure coverage using `.coveragerc` ([#16](../../pull/16))
- Use [nox](https://nox.thea.codes/) for test automation ([#17](../../pull/17))
- Add command-line client ([#21](../../pull/21))
- Add Docker Compose file for development ([#22](../../pull/22))

### Changed
- Switch to `src` layout ([#18](../../pull/18))
- Change adminer port to 9001 ([#11](../../pull/11))
- Upgrade requirements:
  - alembic 1.0.11
  - bcrypt 3.1.7
  - environs 5.2.0
  - flask 1.1.1
  - flask-cors 3.0.8
  - flask-httpauth 3.3.0
  - flask-migrate 2.5.2
  - mako 1.1.0
  - marshmallow 3.0.0rc9
  - psycopg2-binary 2.8.3
  - python-dotenv 0.10.3
  - sqlalchemy 1.3.6
  - werkzeug 0.15.5
- Upgrade test requirements:
  - coverage 4.5.4
  - factory-boy 2.12.0
  - faker 2.0.0
  - importlib-metadata 0.19
  - more-itertools 7.2.0
  - packaging 19.1
  - pluggy 0.12.0
  - pyparsing 2.4.2
  - pytest 5.0.1
  - six 1.12.0
  - wcwidth 0.1.7
  - zipp 0.5.2

### Removed
- Remove extras_require from setup.py ([#20](../../pull/20))
- Remove `http` script (replaced by command-line client).
- Remove Makefile (replaced by nox).
- Remove dev requirements:
  - black
  - click (moved to base requirements)
  - coveralls
  - flake8
  - flake8-bugbear
  - pip-tools

## [0.3.0] - 2019-05-05
### Added
- Add Dockerfile.
- Add Docker Compose file.

### Changed
- Do not generate hashes for requirements.
- Upgrade requirements.

## [0.2.0] - 2018-12-25
### Added
- Add artist resource.
- Add sample env file.
- New configuration settings:
  - `ADMIN_EMAIL`
  - `ADMIN_PASSWORD`
  - `ADMIN_USERNAME`
- Provide Docker stack for postgres service.
- Add logging.
- Add command to create admin user.
- Add httpie wrapper script for authentication.

### Changed
- Format code using [black](https://github.com/ambv/black).
- Unify error handling using `APIError` exception.
- Add helper functions in `muckr.utils`.
- Use flake8-bugbear for linting.
- Return HTTP status code 422 if JSON contains unknown keys.
- Upgrade:
  - marshmallow 3.0.0rc1

### Removed
- Remove trivial make targets.
- Remove `bumpversion.sh` wrapper script.
- Remove unused requirement `marshmallow-jsonapi`.

### Fixed
- Fix typo in `make heroku-db-upgrade`.
- Fix wrong password field type in user schema.

## 0.1.0 - 2018-12-22
### Added
- Initial version.

[Unreleased]: https://github.com/cjolowicz/muckr-api/compare/v0.6.0...HEAD
[0.6.0]: https://github.com/cjolowicz/muckr-api/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/cjolowicz/muckr-api/compare/v0.4.2...v0.5.0
[0.4.2]: https://github.com/cjolowicz/muckr-api/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/cjolowicz/muckr-api/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/cjolowicz/muckr-api/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/cjolowicz/muckr-api/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/cjolowicz/muckr-api/compare/v0.1.0...v0.2.0
