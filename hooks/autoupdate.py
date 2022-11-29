import subprocess
from rich import print as rprint


def main(args):
    # Get the current version of pip
    current_pip = (
        subprocess.check_output(["pip", "--version"])
        .decode("utf-8")
        .split(" ")[1]
        .strip()
    )

    # Get the latest version of pip
    # catch error from standard error
    try:
        subprocess.check_output(
            ["pip", "install", "pip=="], stderr=subprocess.STDOUT
        ).decode("utf-8")
    except subprocess.CalledProcessError as e:
        # extract the version number from the error message
        latest_pip = e.output.decode("utf-8").split(")")[0].split(",")[-1].strip()

    # If the latest version is not the same as the current version, upgrade pip
    if latest_pip != current_pip:
        subprocess.Popen(["python", "-m", "pip", "install", "--upgrade", "pip"])
        rprint(
            f"[italic green]pre-pip[/italic green] updated pip from [italic cyan]{current_pip}[/italic cyan] to [italic cyan]{latest_pip}[/italic cyan]!",
        )
