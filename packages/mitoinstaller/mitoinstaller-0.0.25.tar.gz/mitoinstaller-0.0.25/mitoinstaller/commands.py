"""
Contains useful commands for interacting
with the command line directly
"""

from mitoinstaller.colors import NORMAL_TEXT, RED_TEXT
import subprocess
import sys

def jupyter_labextension_list():
    """
    Returns the stdout, stderr pair for the currently
    installed jupyterlab extensions.
    """

    sys_call = [sys.executable, "-m", "jupyter", "labextension", "list"]

    completed_process = subprocess.run(sys_call, capture_output=True)
    return completed_process.stdout.decode(), completed_process.stderr.decode()


def uninstall_labextension(extension):
    """
    Uninstall a labextension
    """

    sys_call = [sys.executable, "-m", "jupyter", "labextension", "uninstall", extension]

    # Do we want want a check_call?
    # This runs the command that we construct above
    subprocess.check_call(sys_call)


def uninstall_pip_packages(*packages):
    """
    This function uninstalls the given packages in a single pass
    using pip, through the command line.
    """

    sys_call = [sys.executable, "-m", "pip", "uninstall", "-y"]

    for package in packages:
        sys_call.append(package)

    # Do we want want a check_call?
    # This runs the command that we construct above
    subprocess.check_call(sys_call)


def install_pip_packages(*packages):
    """
    This function installs the given packages in a single pass
    using pip, through the command line.

    https://stackoverflow.com/questions/12332975/installing-python-module-within-code
    """

    sys_call = [sys.executable, "-m", "pip", "install"]

    for package in packages:
        sys_call.append(package)

    sys_call.append('--upgrade')

    # Do we want want a check_call?
    # This runs the command that we construct above
    subprocess.check_call(sys_call)

def upgrade_mito_installer():
    """
    Upgrades the mito installer package itself
    """
    # Do we want want a check_call?
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'mitoinstaller', '--upgrade', '--no-cache-dir'])

def exit_with_error(action, error=None):
    # Action should either be install or upgarde

    full_error = f'\n\nSorry, looks like we hit a problem during {action}. ' + \
        ('' if error is None else ("It seems we " + error + '.')) + \
        '\nWe\'re happy to help you fix it, just shoot an email to jake@sagacollab.com and copy in the output above.\n'

    # NOTE: we make the error red, and then switch back to normal text color
    print(RED_TEXT + full_error + NORMAL_TEXT)
    exit(1)