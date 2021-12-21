import subprocess
import shared
import sys


def main():
    shared.configure_python_path()
    if sys.platform.startswith("linux"):
        subprocess.check_call(["sh", "scripts/parsergenerator.sh", shared.SCRIPTS])
    subprocess.check_call(["python", "-m", "py.test", "-vv", "-s", shared.TESTS])


if __name__ == "__main__":
    main()
