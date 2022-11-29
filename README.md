# Pre-pip

Pre-pip is a simple tool that can be used to run something before a pip command is executed.

Currently only `zsh` is supported.

## Installation

```sh
pip install pre-pip
```

## Usage

Install pre-pip using:

```sh
pre-pip install
```

# register a hook

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

## Uninstall

Uninstall pre-pip using:

```sh
pre-pip uninstall
```
