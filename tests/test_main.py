import click.testing
from muckr_api.__main__ import main


def test_hello_world():
    runner = click.testing.CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
