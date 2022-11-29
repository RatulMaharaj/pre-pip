import os
import sys
import click
from pathlib import Path
from rich import print as rprint
from .uninstall import uninstall as uninstall_pre_pip
from .install import install as install_pre_pip
from . import HOOKS_DIR, scaffold_hooks_dir
from . import __version__


@click.group()
@click.version_option(__version__)
@click.pass_context
def cli(ctx):
    """Welcome to the pre-pip CLI!"""
    pass


@cli.command()
def install():
    """Add pre-pip to your shell."""
    scaffold_hooks_dir(HOOKS_DIR)
    install_pre_pip()


@cli.command()
def uninstall():
    """Remove pre-pip from your shell."""
    value = click.prompt(
        "Are you sure you want to uninstall pre-pip? (y/n)",
        type=bool,
    )
    if value:
        uninstall_pre_pip()
        rprint("[italic green]pre-pip[/italic green] was successfully uninstalled!")


@cli.command()
@click.argument("hook", type=click.Path(exists=True), required=True, nargs=1)
def add(hook):
    """Add a pre-pip hook."""
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

        rprint(f"[italic green]pre-pip[/italic green] hook added successfully!")


@cli.command()
def list():
    """See installed pre-pip hooks."""
    hooks = os.listdir(HOOKS_DIR)
    if len(hooks) == 1:
        # i.e. only __init__.py
        rprint("No hooks found.")
    else:
        for hook in hooks:
            if hook.endswith(".py") and hook != "__init__.py":
                rprint(f"[italic cyan]{hook.replace('.py', '')}[/italic cyan]")


@cli.command()
@click.option("--all", is_flag=True, help="Remove all pre-pip hooks.")
@click.argument("hook", nargs=1, required=False)
def remove(hook, all):
    """Remove a pre-pip hook."""
    if all:
        # remove all hooks
        hooks = os.listdir(HOOKS_DIR)
        for hook in hooks:
            if hook.endswith(".py") and hook != "__init__.py":
                os.remove(os.path.join(HOOKS_DIR, hook))

        # reset __init__.py
        with open(os.path.join(HOOKS_DIR, "__init__.py"), "w") as f:
            f.write("")

        rprint("All hooks removed successfully!")
    else:
        if hook is None:
            rprint(
                "[bold red]ERROR:[/bold red] Please specify a hook or use the --all flag."
            )
            sys.exit()
        else:
            # remove specified hook
            if os.path.isfile(os.path.join(HOOKS_DIR, f"{hook}.py")):
                os.remove(os.path.join(HOOKS_DIR, f"{hook}.py"))

                # remove the import statement from __init__.py
                with open(os.path.join(HOOKS_DIR, "__init__.py"), "r") as f:
                    lines = f.readlines()

                with open(os.path.join(HOOKS_DIR, "__init__.py"), "w") as f:
                    for line in lines:
                        if f"from .{hook} import main as {hook}" not in line:
                            f.write(line)

                rprint(
                    f"[italic green]pre-pip[/italic green] hook removed successfully!"
                )


if __name__ == "__main__":
    cli()
