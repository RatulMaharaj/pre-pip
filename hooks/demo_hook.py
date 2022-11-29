from rich import print as rprint


def main(args):
    rprint(
        f"The [italic green]pre-pip[/italic green] demo_hook received: [italic cyan]{args}[/italic cyan]",
    )
