import os
import sys
import subprocess
from rich import print as rprint


pre_pip_script = r"""# pre-pip start
preexec () {
    # check if $1 contains pip
    if [[ "$1" = "pip"* ]]; then
        # call python function
        python3 -c "import pre_pip; pre_pip.main('$1')"
    fi
    return 0
}
# pre-pip end
"""


def install():
    # Check which shell is running
    shell = os.environ.get("SHELL", "sh")

    if "zsh" in shell:
        install_rc("zsh")
    elif "bash" in shell:
        install_bash_preexec()
        install_rc("bash")
    else:
        rprint(
            f"[italic green]pre-pip[/italic green] is unfortunately not currently supported for {shell}."
        )
        sys.exit()


def install_rc(shell: str):
    if shell not in ["bash", "zsh"]:
        rprint(
            f"[italic green]pre-pip[/italic green] is unfortunately not currently supported for {shell}."
        )
        sys.exit()

    # check if rc file exists
    if not os.path.isfile(os.path.expanduser(f"~/.{shell}rc")):
        # create it if it doesn't exist
        with open(os.path.expanduser(f"~/.{shell}rc"), "w") as f:
            f.write("")

    # check for pre-pip in .zshrc
    with open(os.path.expanduser(f"~/.{shell}rc"), "r") as f:
        shell_rc = f.read()

    if "pre-pip" not in shell_rc:
        # installing pre-pip
        with open(os.path.expanduser(f"~/.{shell}rc"), "a") as f:
            f.write("\n")
            f.write(pre_pip_script)

        rprint("[italic green]pre-pip[/italic green] was installed! \n")

        # ask to reload shell rc file
        rprint(
            f"Please run `[cyan]source ~/.{shell}rc[/cyan]` to reload your configuration."
        )
    else:
        rprint("[italic green]pre-pip[/italic green] is already installed!")


def install_bash_preexec():
    # check if .bashrc exists
    if not os.path.isfile(os.path.expanduser("~/.bashrc")):
        # create .bashrc if it doesn't exist
        with open(os.path.expanduser("~/.bashrc"), "w") as f:
            f.write("")

    # check if .bash-preexec.sh exists
    if not os.path.isfile(os.path.expanduser("~/.bash-preexec.sh")):
        # Save .bash-preexec.sh to ~/.bash-preexec.sh
        subprocess.Popen(
            [
                "wget",
                "-O",
                "~/.bash-preexec.sh",
                "https://raw.githubusercontent.com/rcaloras/bash-preexec/master/bash-preexec.sh",
            ]
        )

    # check if .bashrc contains the source command
    with open(os.path.expanduser("~/.bashrc"), "r") as f:
        if "bash-preexec.sh" not in f.read():
            # if not, add the source command to .bashrc
            print("adding source command to .bashrc")
            with open(os.path.expanduser("~/.bashrc"), "a") as f:
                f.write("[[ -f ~/.bash-preexec.sh ]] && source ~/.bash-preexec.sh")


if __name__ == "__main__":
    install()
