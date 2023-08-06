"""
We specify the installer as a list of steps that 
must run in order, for the installer.

Currently, we take the following steps:
1. First, try and install mitosheet3. Because mitosheet3 uses 
   JLab 3, we first check if the user has any conflicting
   JLab 2 dependencies installed. If they do, we abort. If they 
   don't, we update them to JLab 3.
2. Then, if the above installation of mitosheet3 fails for 
   any reason, we try to install mitosheet on JLab 2. 
3. If neither of them work, we give up, sadly. 
"""

import traceback
from mitoinstaller.colors import NORMAL_TEXT, GREEN_TEXT
from mitoinstaller.commands import install_pip_packages, jupyter_labextension_list, uninstall_labextension, uninstall_pip_packages, upgrade_mito_installer, exit_with_error
from mitoinstaller.log_utils import log, identify, log_step_failed
from mitoinstaller.user_install import (try_create_user_json_file, get_static_user_id, set_user_field)
from mitoinstaller import __version__

# SHARED UTILITIES

def initial_install_step_create_user(install_or_upgrade):
    static_user_id = get_static_user_id()

    # If the user has no static install ID, create one
    if static_user_id is None:
        try_create_user_json_file()    
    
    identify()
    log(f'{install_or_upgrade}_started', {
        'mitoinstaller_version': __version__
    })

def get_extension_names_from_labextension_list_output(stdout, stderr):
    """
    Returns a list of the extension names installed from the stdout, stderr
    pair returned from the jupyter labextension list.

    If you run the command: `jupyter labextension list`, the output is: 
    ------
    JupyterLab v0.35.0
    Known labextensions:
    app dir: /Users/nate/saga-vcs/monorepo/mito/installer/venv/share/jupyter/lab
            @jupyter-widgets/jupyterlab-manager v0.38.1 enabled OK
    ------

    Note that part of this output prints to stdout, and other parts to stderr 
    (for some reason), so we append them with a newline so we make sure we 
    get all of the extensions correctly!
    """
    def is_extension_line(line):
        # Check that it has a version
        if len(line) == 0:
            return False

        if 'v' not in line:
            return False
        
        # Check that it is either enabled or disabled
        return 'enabled' in line or 'disabled' in line

    output = stdout + "\n" + stderr
    extension_lines = [line.strip() for line in output.splitlines() if is_extension_line(line)]
    extension_names = []
    for line in extension_lines:
        extension_names.append(line.split(" ")[0])

    return extension_names

def get_jupyterlab_metadata():
    """
    Helper function that returns a tuple of: (jupyterlab_version), (installed_extensions)

    If no JupyterLab is installed, returns (None, None)
    """
    try:
        from jupyterlab import __version__
    except Exception as e:
        # If this import fails, it must not be installed
        return None, None

    stdout, stderr = jupyter_labextension_list()
    extension_names = get_extension_names_from_labextension_list_output(stdout, stderr)
    return __version__, extension_names


# MITOSHEET 3 INSTALL STEPS

def install_step_mitosheet3_check_dependencies():
    """
    This is the most complex step in the installation process. It's
    goal is to check if the users existing installation can safely
    be upgraded to JLab 3.0. 

    To do this, it checks a variety of conditions, mostly around what
    version of JLab they have installed, and if this version of JLab has
    any installed dependencies (that we cannot safely upgrade).
    """

    jupyterlab_version, extension_names = get_jupyterlab_metadata()

    # If no JupyterLab is installed, we can continue with install, as
    # there are no conflict dependencies
    if jupyterlab_version is None:
        return
    
    # If JupyterLab 3 is installed, then we are are also good to go
    if jupyterlab_version.startswith('3'):
        return
    
    if len(extension_names) == 0:
        return
    elif len(extension_names) == 1 and extension_names[0] == 'mitosheet':
        uninstall_labextension('mitosheet')
        uninstall_pip_packages('mitosheet')
        log('uninstalled_mitosheet_labextension',
            {
                'jupyterlab_version': jupyterlab_version,
                'extension_names': extension_names
            }
        )
        return
    else:
        raise Exception(f'Installed extensions {extension_names}')


def install_step_mitosheet3_install_mitosheet3():
    install_pip_packages('mitosheet3')


INSTALL_MITOSHEET3_STEPS = [
    {
        'step_name': 'check dependencies',
        'execute': install_step_mitosheet3_check_dependencies
    },
    {
        'step_name': 'install mitosheet3',
        'execute': install_step_mitosheet3_install_mitosheet3
    },
]


# MITOSHEET 2 INSTALL STEPS


def install_step_mitosheet_check_dependencies():
    jupyterlab_version, extension_names = get_jupyterlab_metadata()

    # If no JupyterLab is installed, we can continue with install, as
    # there are no conflict dependencies
    if jupyterlab_version is None:
        return
    
    # If JupyterLab 2 is installed, then we are are also good to go
    if jupyterlab_version.startswith('2'):
        return
    
    if len(extension_names) == 0:
        return
    elif len(extension_names) == 1 and extension_names[0] == 'mitosheet':
        return
    else:
        raise Exception(f'Installed extensions {extension_names}')


def install_step_mitosheet_install_mitosheet():
    install_pip_packages('mitosheet')


def install_step_mitosheet_install_jupyter_widget_manager():
    from jupyterlab import commands
    commands.install_extension('@jupyter-widgets/jupyterlab-manager@2')


def install_step_mitosheet_rebuild_jupyterlab():
    from jupyterlab import commands
    commands.build()


def install_step_mitosheet_upgrade_mitoinstaller():
    upgrade_mito_installer()


INSTALL_MITOSHEET_STEPS = [
    {
        'step_name': 'upgrade mitoinstaller',
        'execute': install_step_mitosheet_upgrade_mitoinstaller
    },
    {
        'step_name': 'check dependencies',
        'execute': install_step_mitosheet_check_dependencies
    },
    {
        'step_name': 'install mitosheet',
        'execute': install_step_mitosheet_install_mitosheet
    },
    {
        'step_name': 'install @jupyter-widgets/jupyterlab-manager@2',
        'execute': install_step_mitosheet_install_jupyter_widget_manager
    },
    {
        'step_name': 'rebuild JupyterLab',
        'execute': install_step_mitosheet_rebuild_jupyterlab
    },
]

def do_install_or_upgrade(install_or_upgrade):
    """
    install_or_upgrade is the workhorse of actually installing mito. It first attempts
    to install mitosheet3, and if that fails, installs mitosheet.

    install_or_upgrade should be 'install' or 'upgrade'

    Notably, the process for installing Mito initially and upgrading Mito are
    identical. As such, we reuse this function to upgrade, just with different
    error and logging messages.
    """
    if install_or_upgrade == 'install':
        success_message = f'\nMito has finished installing. Relaunch JupyterLab to render your first mitosheet. \n\nRun the command:\t{GREEN_TEXT}jupyter lab{NORMAL_TEXT}\n'
    else:
        success_message = f'\nMito has finished upgrading. Relaunch JupyterLab to see new functionality. \n\nRun the command:\t{GREEN_TEXT}jupyter lab{NORMAL_TEXT}\n'
    
    initial_install_step_create_user(install_or_upgrade)

    for idx, install_step in enumerate(INSTALL_MITOSHEET3_STEPS):
        try:
            install_step['execute']()
            # If we finish install, then tell the user, and exit
            if idx >= len(INSTALL_MITOSHEET3_STEPS) - 1:
                set_user_field('install_finished', True)
                log(f'{install_or_upgrade}_finished_mitosheet3', {'package': 'mitosheet3'})
                print(success_message)
                exit(0)
        except SystemExit:
            exit(0)
        except:
            # Note: if mitosheet3 installation fails, we log it, but we do
            # not exit, as we want to continue and try to install mitosheet
            error_message = "failed to " + install_step['step_name']
            log_step_failed(install_or_upgrade, 'mitosheet3', error_message)
            print(error_message)
            # We do break out of this loop!
            break

    for install_step in INSTALL_MITOSHEET_STEPS:
        try:
            install_step['execute']()
        except:
            error_message = "failed to " + install_step['step_name']
            log_step_failed(install_or_upgrade, 'mitosheet', error_message)
            exit_with_error(install_or_upgrade, error_message)

    set_user_field('install_finished', True)
    log(f'{install_or_upgrade}_finished_mitosheet', {'package': 'mitosheet'})
    print(success_message)