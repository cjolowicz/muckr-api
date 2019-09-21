import subprocess

import environs
import pytest

from .client import API


def _console(*args):
    # Disable pseudo-TTY allocation (docker/compose#5696).
    command = "docker-compose", "exec", "-T", "muckr-api", "/venv/bin/muckr-api"
    return subprocess.run(command + args, check=True)


@pytest.fixture(scope="session")
def docker_compose():
    yield subprocess.run(["docker-compose", "up", "--detach"], check=True)
    subprocess.run(["docker-compose", "down"], check=True)


@pytest.fixture(scope="session")
def api(docker_compose):
    api = API("http://localhost:9000")
    api.wait()
    return api


@pytest.fixture(autouse=True)
def reset_database(docker_compose):
    _console("db", "downgrade", "base")
    _console("db", "upgrade")


@pytest.fixture
def admin(api):
    _console("create-admin")

    env = environs.Env()
    env.read_env()

    return {
        "username": env.str("ADMIN_USERNAME", "admin"),
        "password": env.str("ADMIN_PASSWORD"),
    }
