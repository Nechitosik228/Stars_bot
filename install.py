import os
import shutil
import time
from commands import GitHubCommands, VenvCommands


def main():
    entries = os.scandir()
    for item in GitHubCommands:
        print(item)
        os.system(item)
    # os.system(GitHubCommands.PULL.value)

    for entry in entries:
        if entry.name == ".venv":
            shutil.rmtree(entry.name)
            for item in VenvCommands:
                print(item)
                os.system(item)
            break

    else:
        print("No .venv found")

        for item in (
            VenvCommands.CREATE,
            VenvCommands.ACTIVATE,
            VenvCommands.INSTALL_REQUIREMENTS,
        ):
            print(item)
            os.system(item)
        # time.sleep(2)


if __name__ == "__main__":
    main()
