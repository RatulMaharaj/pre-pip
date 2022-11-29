import os
import shutil
from . import HOOKS_DIR


def uninstall():
    # Check which shell is running
    shell = os.environ.get("SHELL", "sh")

    if "zsh" in shell:
        uninstall_zsh()

    # delete hooks dir
    if os.path.isdir(HOOKS_DIR):
        shutil.rmtree(HOOKS_DIR)


def uninstall_zsh():
    # open .zshrc
    with open(os.path.expanduser("~/.zshrc"), "r") as f:
        zshrc = f.read()

        # check for pre-pip in .zshrc
        if "pre-pip" in zshrc:
            # if found, remove it
            # delete all lines between the start and end
            zshrc = zshrc.replace(
                zshrc[
                    zshrc.find("# pre-pip start") : zshrc.find("# pre-pip end")  # noqa
                    + len("# pre-pip end")  # noqa
                ],
                "",
            )

            #  remove black lines at the end of zshrc
            zshrc = zshrc.rstrip()

            # add a new line at the end of zshrc
            zshrc += "\n"

            # write the new .zshrc
            with open(os.path.expanduser("~/.zshrc"), "w") as f:
                f.write(zshrc)


if __name__ == "__main__":
    uninstall()
