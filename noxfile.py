import os

import nox


nox.options.sessions = "lint", "tests"

locations = "migrations", "noxfile.py", "setup.py", "src", "tests", "wsgi.py"


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
    package = os.path.join(
        session.virtualenv.location,
        "lib",
        session.virtualenv._resolved_interpreter,
        "site-packages",
        "muckr_api",
    )
    session.install("-r", "requirements/base.txt")
    session.install("-r", "requirements/tests.txt")
    session.install(".")
    tests = session.posargs or ["tests/"]
    session.run("pytest", f"--cov={package}", *tests)


@nox.session(python="3.7")
def upgrade(session):
    """Upgrade the requirements."""
    session.install("pip-tools")
    for requirements in ["base", "dev", "tests"]:
        basename = os.path.join("requirements", requirements)
        session.run(
            "pip-compile",
            "--verbose",
            "--upgrade",
            f"--output-file={basename}.txt",
            f"{basename}.in",
        )
