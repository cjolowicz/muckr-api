import nox


nox.options.sessions = "lint", "tests"

locations = "migrations", "noxfile.py", "src", "tests", "wsgi.py"


@nox.session(python="3.7")
def black(session):
    """Run black code formatter."""
    session.install("black")
    session.run("black", *locations)


@nox.session(python="3.7")
def lint(session):
    """Lint using flake8."""
    session.install("flake8", "flake8-bugbear", "flake8-import-order", "black")
    session.run("black", "--check", *locations)
    session.run("flake8", *locations)


@nox.session(python="3.7")
def tests(session):
    """Run the test suite."""
    env = {"VIRTUAL_ENV": session.virtualenv.location}
    session.run("poetry", "install", external=True, env=env)
    session.run("pytest", "--cov=muckr_api", *session.posargs)


@nox.session(python="3.7")
def integration_tests(session):
    """Run the integration tests."""
    env = {"VIRTUAL_ENV": session.virtualenv.location}
    session.run("poetry", "install", external=True, env=env)
    session.run(
        "pytest", "-m", "integration_test", "--with-integration-tests", *session.posargs
    )
