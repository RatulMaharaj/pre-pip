import os
import shutil
from . import HOOKS_DIR


def uninstall():
    # Check which shell is running
    shell = os.environ.get("SHELL", "sh")

    if "zsh" in shell:
        uninstall_from_rc("zsh")
    elif "bash" in shell:
        uninstall_from_rc("bash")
    else:
        print("Failed to uninstall from unsupported shell.")

    # delete hooks dir
    if os.path.isdir(HOOKS_DIR):
        shutil.rmtree(HOOKS_DIR)


def uninstall_from_rc(shell: str):
    # open rc file
    with open(os.path.expanduser(f"~/.{shell}rc"), "r") as f:
        rc = f.read()

        # check for pre-pip in .rc
        if "pre-pip" in rc:
            # if found, remove it
            # delete all lines between the start and end
            rc = rc.replace(
                rc[
                    rc.find("# pre-pip start") : rc.find("# pre-pip end")  # noqa
                    + len("# pre-pip end")  # noqa
                ],
                "",
            )

            #  remove black lines at the end of rc
            rc = rc.rstrip()

            # add a new line at the end of rc
            rc += "\n"

            # write the new .rc
            with open(os.path.expanduser(f"~/.{shell}rc"), "w") as f:
                f.write(rc)


if __name__ == "__main__":
    uninstall()
