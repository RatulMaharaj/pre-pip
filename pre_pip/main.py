import os
import sys

# default hooks directory
HOOKS_DIR = os.path.expanduser("~/pre-pip/hooks")


def scaffold_hooks_dir(HOOKS_DIR=HOOKS_DIR):
    # Create hooks dir if it doesn't exist
    if not os.path.isdir(HOOKS_DIR):
        # create all parent directories
        os.makedirs(HOOKS_DIR)

    # Ensure there is an init file in the hooks dir if one doesn't exist
    if not os.path.isfile(os.path.join(HOOKS_DIR, "__init__.py")):
        with open(os.path.join(HOOKS_DIR, "__init__.py"), "w") as f:
            f.write("")


scaffold_hooks_dir(HOOKS_DIR)


def main(args: str):
    #  import hooks package
    sys.path.append(HOOKS_DIR)

    for file in os.listdir(HOOKS_DIR):
        if file.endswith(".py") and file != "__init__.py":
            #  import hook
            hook = __import__(file.rstrip(".py"))
            #  run hook
            hook.main(args)


if __name__ == "__main__":
    main()
