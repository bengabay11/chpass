import subprocess
import sys
from termcolor import colored


def get_current_package_version(package_name: str) -> str:
    current_version = str(subprocess.run([sys.executable, '-m', 'pip', 'show', '{}'.format(package_name)],
                                         capture_output=True, text=True))
    current_version = current_version[current_version.find('Version:') + 8:]
    return current_version[:current_version.find('\\n')].replace(' ', '')


def get_latest_package_version(package_name: str) -> str:
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', '{}==random'.format(package_name)],
                                        capture_output=True, text=True))
    latest_version = latest_version[latest_version.find('(from versions:') + 15:]
    latest_version = latest_version[:latest_version.find(')')]
    return latest_version.replace(' ', '').split(',')[-1]


def check_latest_package_version(package_name: str) -> None:
    current_version = get_current_package_version(package_name)
    latest_version = get_latest_package_version(package_name)
    if current_version < latest_version:
        print(colored("Warning:", "yellow"), f"There is a newer version for {package_name}."
                                             f" current: ({current_version}), latest: ({latest_version})")
        print(f"You should try update by running the command: pip install -U {package_name}")
