import os
from click.testing import CliRunner
from pre_pip.cli import install, uninstall, add, list, remove
import subprocess


def test_install():
    """Test installing pre-pip."""
    runner = CliRunner()
    result = runner.invoke(install)
    assert result.exit_code == 0
    assert (
        "pre-pip was installed!" in result.output
        or "pre-pip is already installed!" in result.output  # noqa
    )


def test_add():
    """Test adding a pre-pip hook."""
    runner = CliRunner()
    result = runner.invoke(add, ["tests/hooks/test_hook.py"])
    assert result.exit_code == 0
    assert "pre-pip hook added successfully!" in result.output

    #  check that pre-pip folder was created
    assert os.path.isdir(os.path.expanduser("~/pre-pip"))

    # check that the hooks subfolder was created
    assert os.path.isdir(os.path.expanduser("~/pre-pip/hooks"))

    # check that the hook was copied to the hooks subfolder
    assert os.path.isfile(os.path.expanduser("~/pre-pip/hooks/test_hook.py"))

    # check that there is an __init__.py file in the hooks subfolder
    assert os.path.isfile(os.path.expanduser("~/pre-pip/hooks/__init__.py"))

    # check that the hook was added to the __init__.py file
    with open(os.path.expanduser("~/pre-pip/hooks/__init__.py"), "r") as f:
        init_file = f.read()

    # Check if the correct import was added to the __init__.py file
    assert "from .test_hook import main as test_hook" in init_file


def test_list():
    """Test listing pre-pip hooks."""
    runner = CliRunner()
    result = runner.invoke(list)
    assert result.exit_code == 0
    assert "test_hook" in result.output


def test_remove():
    """Test removing a pre-pip hook."""
    runner = CliRunner()
    result = runner.invoke(remove, ["test_hook"])
    assert result.exit_code == 0
    assert "pre-pip hook removed successfully!" in result.output

    # check that the hook was removed from the __init__.py file
    with open(os.path.expanduser("~/pre-pip/hooks/__init__.py"), "r") as f:
        init_file = f.read()

    # Check if the correct import was removed from the __init__.py file
    assert "from .test_hook import main as test_hook" not in init_file

    # check that the hook was removed from the hooks subfolder
    assert not os.path.isfile(os.path.expanduser("~/pre-pip/hooks/test_hook.py"))

    # check that the hooks subfolder is empty
    assert len(os.listdir(os.path.expanduser("~/pre-pip/hooks"))) == 1


def test_uninstall():
    """Test uninstalling pre-pip."""
    runner = CliRunner()
    result = runner.invoke(uninstall, ["--no-prompt"])
    assert result.exit_code == 0
    assert "pre-pip was successfully uninstalled!" in result.output
