"""
Useful functions and utilities for
logging information about install
"""
import traceback
import analytics
import platform

analytics.write_key = '6I7ptc5wcIGC4WZ0N1t0NXvvAbjRGUgX' 

from mitoinstaller.user_install import get_static_user_id_install

def identify():
    """
    Note: this assumes the user_install.json has been 
    created!
    """
    static_user_id_install = get_static_user_id_install()
    operating_system = platform.system()

    analytics.identify(
        static_user_id_install,
        {
            'operating_system': operating_system
        }
    )

def log_step_failed(install_or_upgrade, package, reason):
    log(
        f'{install_or_upgrade}_failed_{package}',
        {  
            'package': package,
            'reason': reason, 
            'error_traceback': traceback.format_exc().split('\n')
        }
    )

def log(event, params=None):
    """
    A utility that all logging should pass through
    """
    static_user_id_install = get_static_user_id_install()

    if params is None:
        params = {}

    analytics.track(
        static_user_id_install, 
        event, 
        params
    )
