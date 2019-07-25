# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Enable CI for pull requests ([#13](../../pull/13))
- Configure Heroku review apps using `app.json` ([#15](../../pull/15))
- Configure coverage using `.coveragerc` ([#16](../../pull/16))

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

[Unreleased]: https://github.com/cjolowicz/muckr-service/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/cjolowicz/muckr-service/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/cjolowicz/muckr-service/compare/v0.1.0...v0.2.0
