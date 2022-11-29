<p align="center" style="height: 3em;">
    <img src="pre-pip.svg" alt="pre-pip" align="center"></img>
</p>
<p align="center">
    <em>Run some python code just before your pip commands.</em>
</p>

<p align="center">    
<a href="https://github.com/RatulMaharaj/pre-pip/actions/workflows/python-publish.yml" target="_blank">
    <img src="https://github.com/RatulMaharaj/pre-pip/actions/workflows/python-publish.yml/badge.svg" alt="Publish">
</a>
<a href="https://pypi.org/project/pre-pip" target="_blank">
    <img src="https://img.shields.io/pypi/v/pre-pip?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

<hr/>

### Use cases

- Before installing a package, check it against a list of known malicious packages.
- Upgrade pip automatically before installing a package.
- Inject pip proxy settings into the environment before installing a package.

You can use it to run any custom python code before a pip command is executed.

### Supported shells

Currently only `zsh` is supported, I'm currently working on adding support `bash` and `powershell`.

Contributions for any other shells are welcome.

### Installation

```sh
pip install pre-pip
```

There is potential to make this `pipx` installable.

### Usage

Install `pre-pip` into your `.*rc` file using:

```sh
pre-pip install
```

### Register a custom demo hook

Create a new file called `demo.py` in your current directory with the following content:

```python
from rich import print as rprint


def main(args):
    rprint(
        f"This [italic green]pre-pip[/italic green] hook received: [italic cyan]{args}[/italic cyan]",
    )

```

Register the hook using:

```sh
pre-pip add ./demo.py
```

You can view the list of registered hooks using:

```sh
pre-pip list
```

### Uninstall

Uninstall `pre-pip` using:

```sh
pre-pip uninstall
```

This will remove the `pre-pip` hook from your `.*rc` file as well as all registered hooks.

To remove the pre-pip package, use:

```sh
pip uninstall pre-pip
```

### License

[MIT](LICENSE)
