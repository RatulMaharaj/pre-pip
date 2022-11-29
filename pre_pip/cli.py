"""Command Line Interface for pre-pip."""
import os
import sys
import click
from pathlib import Path
from rich import print as rprint
from .uninstall import uninstall as uninstall_pre_pip
from .install import install as install_pre_pip
from . import HOOKS_DIR, scaffold_hooks_dir


@click.group()
def cli():
    pass


@cli.command()
def install():
    """Install pre-pip"""
    scaffold_hooks_dir(HOOKS_DIR)
    install_pre_pip()


@cli.command()
def uninstall():
    """Uninstall pre-pip"""
    value = click.prompt(
        "Are you sure you want to uninstall pre-pip? (y/n)",
        type=bool,
    )
    if value:
        uninstall_pre_pip()
        rprint("[italic green]pre-pip[/italic green] was successfully uninstalled!")


@cli.command()
@click.argument("hook")
def register(hook):
    """Register a pre-pip hook"""
    # check if hook exists
    if not os.path.isfile(hook):
        rprint(
            f"[bold red]ERROR:[/bold red] Specified hook [italic cyan]{hook}[/italic cyan] does not exist!"
        )
        sys.exit()
    else:
        # if it does, copy it to HOOKS_DIR
        os.system(f"cp {hook} {HOOKS_DIR}")

        hook_no_ext = Path(hook).stem

        # update the init file
        with open(os.path.join(HOOKS_DIR, "__init__.py"), "r") as f:
            import_statement = f"from .{hook_no_ext} import main as {hook_no_ext}"
            # check if the import statement already exists
            if import_statement not in f.read():
                with open(os.path.join(HOOKS_DIR, "__init__.py"), "a") as f:
                    f.write(import_statement)
                    f.write("\n")

    rprint(f"[italic green]pre-pip[/italic green] hook successfully registered!")


@cli.command()
def list():
    """List installed pre-pip hooks"""
    hooks = os.listdir(HOOKS_DIR)
    if len(hooks) == 1:
        rprint("No hooks found.")
    else:
        for hook in hooks:
            if hook.endswith(".py") and hook != "__init__.py":
                rprint(f"[italic cyan]{hook.replace('.py', '')}[/italic cyan]")


@cli.command()
def run():
    """Run a pre-pip hook"""
    rprint("Running pre-pip hooks.")


if __name__ == "__main__":
    cli()
