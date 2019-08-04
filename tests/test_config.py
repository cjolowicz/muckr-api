"""Test config."""
import os

import environs
import pytest


@pytest.mark.usefixtures("app")
class TestConfig:
    def test_config_requires_secret_key(self):
        try:
            del os.environ["SECRET_KEY"]
        except KeyError:
            pass

        env = environs.Env()
        env.read_env()

        if "SECRET_KEY" in os.environ:
            pytest.skip("SECRET_KEY set in .env file")

        with pytest.raises(environs.EnvError):
            import muckr_api.config  # noqa

    def test_config_reads_environment_variables(self):
        os.environ["ADMIN_PASSWORD"] = "password"
        os.environ["DATABASE_URL"] = "sqlite://"
        os.environ["SECRET_KEY"] = "secret-key"

        import muckr_api.config

        assert muckr_api.config.SECRET_KEY == "secret-key"
        assert muckr_api.config.SQLALCHEMY_DATABASE_URI == "sqlite://"
