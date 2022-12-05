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
@click.version_option(__version__, message="pre-pip %(version)s")
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
@click.option("--no-prompt", "-np", is_flag=True, help="Do not prompt.")
def uninstall(no_prompt):
    """Remove pre-pip from your shell."""
    if not no_prompt:
        value = click.prompt(
            "Are you sure you want to uninstall pre-pip? (y/n)",
            type=bool,
        )
        if not value:
            sys.exit()
    uninstall_pre_pip()
    rprint("[italic green]pre-pip[/italic green] was successfully uninstalled!")


@cli.command()
@click.argument("hook", required=True, nargs=1)
@click.option("--no-prompt", "-np", is_flag=True, help="Do not prompt.")
def add(hook, no_prompt):
    """Add a pre-pip hook."""
    # check if url or path
    if hook.startswith("http") and hook.endswith(".py"):
        # download hook to hooks dir using curl
        try:
            rprint(
                "[bold yellow]WARNING![/bold yellow] You are about to download arbitrary code from the internet."
            )
            if not no_prompt:
                # prompt user to continue
                value = click.prompt(
                    "Do you trust the source and want to proceed? (y/n)",
                    type=bool,
                )
                if not value:
                    sys.exit()

            os.system(f"curl -s {hook} -o {HOOKS_DIR}/{Path(hook).name}")
        except Exception:
            rprint(
                f"[italic red]Error:[/italic red] Failed to download hook from [italic cyan]{hook}[/italic cyan]"
            )
            sys.exit()
    else:
        # check if hook exists
        if not os.path.isfile(hook):
            rprint(
                f"[bold red]ERROR:[/bold red] Specified hook [italic cyan]{hook}[/italic cyan] does not exist or is invalid!"
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

    rprint("[italic green]pre-pip[/italic green] hook added successfully!")


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
                    "[italic green]pre-pip[/italic green] hook removed successfully!"
                )


if __name__ == "__main__":
    cli()
