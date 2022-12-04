import os
from click.testing import CliRunner
from pre_pip.cli import install, uninstall


def test_uninstall():
    """Test uninstalling pre-pip."""
    runner = CliRunner()
    result = runner.invoke(uninstall, ["--no-prompt"])
    assert result.exit_code == 0
    assert "pre-pip was successfully uninstalled!" in result.output


def test_install():
    """Test installing pre-pip."""
    runner = CliRunner()
    result = runner.invoke(install)
    assert result.exit_code == 0
    assert "pre-pip was installed!" in result.output


def test_install_when_already_installed():
    """Test installing pre-pip when it's already installed."""
    runner = CliRunner()
    result = runner.invoke(install)
    assert result.exit_code == 0
    assert "pre-pip is already installed!" in result.output


def test_install_to_rc():
    """Test installing pre-pip to rc file."""
    shell = os.environ.get("SHELL", "sh").split("/")[-1].lower()
    with open(os.path.expanduser(f"~/.{shell}rc"), "r") as f:
        shell_rc = f.read()
    assert "pre-pip" in shell_rc


def test_uninstall_from_rc():
    """Test uninstalling pre-pip."""
    runner = CliRunner()
    result = runner.invoke(uninstall, ["--no-prompt"])
    assert result.exit_code == 0
    assert "pre-pip was successfully uninstalled!" in result.output

    shell = os.environ.get("SHELL", "sh").split("/")[-1].lower()
    with open(os.path.expanduser(f"~/.{shell}rc"), "r") as f:
        shell_rc = f.read()
    assert "pre-pip" not in shell_rc
