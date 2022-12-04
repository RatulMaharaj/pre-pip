from pre_pip import __version__, __author__, __email__


def check_meta():
    assert __author__ == "Ratul Maharaj"
    assert __email__ == "ratulmaharaj@looped.co.za"


def test_version():
    """Check that the version is correctly set everywhere."""
    # check version in pyproject.toml
    with open("pyproject.toml", "r") as f:
        pyproject = f.read()

    assert f'version = "{__version__}"' in pyproject
