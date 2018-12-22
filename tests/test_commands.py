import muckr.commands
from muckr.user.models import User


def test_create_admin_inserts_admin_user(app, database):
    runner = app.test_cli_runner()
    result = runner.invoke(muckr.commands.create_admin, catch_exceptions=False)
    assert result.exit_code == 0
    assert 'admin' in {
        user.username for user in User.query.all()
    }
