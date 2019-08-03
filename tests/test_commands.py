import pytest

import muckr.commands
from muckr.user.models import User


def test_create_admin_inserts_admin_user(app, database):
    runner = app.test_cli_runner()
    result = runner.invoke(muckr.commands.create_admin, catch_exceptions=False)
    assert result.exit_code == 0
    assert "admin" in {user.username for user in User.query.all()}


@pytest.mark.parametrize(
    "url", ["https://muckr-service.herokuapp.com/artists", "https://localhost/artists"]
)
def test_client_succeeds(app, mocker, url):
    mocker.patch("subprocess.run").return_value.stdout = '{"ADMIN_PASSWORD": ""}'
    mocker.patch("requests.post").return_value.json.return_value = {"token": ""}
    runner = app.test_cli_runner()
    result = runner.invoke(muckr.commands.client, ["GET", url], catch_exceptions=False)
    assert result.exit_code == 0
