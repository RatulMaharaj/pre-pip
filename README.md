## Pre-pip

`pre-pip` is a tool that allows you to run something before a pip command is executed.

### Suggested use cases:

- Before installing a package, check it against a list of known malicious packages.
- Upgrade pip automatically before installing a package.

You can use it to run any custom python code before a pip command is executed.

### Supported terminals

Currently only `zsh` is supported.

Contributions for other shells are welcome.

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

Create a new file called demo_hook.py in your current directory with the following content:

```python
from rich import print as rprint


def main(args):
    rprint(
        f"This [italic green]pre-pip[/italic green] hook received: [italic cyan]{args}[/italic cyan]",
    )

```

Register the hook using:

```sh
pre-pip register ./demo_hook.py
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
