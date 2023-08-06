import os
import uuid
import json
from mitoinstaller import __version__
from datetime import datetime

# Where all global .mito files are stored
MITO_FOLDER = os.path.expanduser("~/.mito")

# The path of the user.json file, which notably is the same
# path as the USER_JSON_PATH in mitosheet
USER_JSON_PATH = os.path.join(MITO_FOLDER, 'user.json')

def get_random_id():
    """
    Creates a new random ID for the user, which for any given user,
    should only happen once.
    """
    return str(uuid.uuid1())

# NOT: This must stay in sync with the object in the mitoinstaller
# package! There are some missing fields which are explicitly noted
# below
# This is the default user json object
USER_JSON_DEFAULT = {
    'user_json_version': 1,
    'static_user_id': '',
    # A random secret that the user can use as salt when hashing things
    'user_salt': get_random_id(),
    'user_email': '',
    # A list of actions the user intends to do on the tool, which they fill
    # out when they sign up
    'intended_behavior': [],
    'received_tours': [],
    # A list of all the feedback the user has given
    'feedbacks': [],
    # If the user opted out of feedback, we store that they opted out, so
    # that we don't bombard them with feedback
    'closed_feedback': False,
    # NOTE: we leave out some feilds that we want to set at runtime
    # of mito. Specifically: mitosheet_current_version, mitosheet_last_upgraded_date, and 
    # mitosheet_last_five_usages
}

# NOTE: This function must stay in sync with the same file in the
# mitosheet package
def try_create_user_json_file():
    # Create the mito folder if it does not exist
    if not os.path.exists(MITO_FOLDER):
        os.mkdir(MITO_FOLDER)
        
    # We only create a user.json file if it does not exist
    if not os.path.exists(USER_JSON_PATH):
        # First, we write an empty default object
        with open(USER_JSON_PATH, 'w+') as f:
            f.write(json.dumps(USER_JSON_DEFAULT))

        # Then, we create a new static id and capture the email for the user. 
        # We take special care to put all the CI enviornments 
        # (e.g. Github actions) under one ID and email
        if 'CI' in os.environ and os.environ['CI'] is not None:
            static_user_id = 'github_action'
            user_email = 'github@action.com'
        else:
            # Take the static user id from the installer, if it exists, and otherwise
            # generate a new one
            static_user_id = get_random_id()
            # We used to read the user email if they were signed in on a kubernetes
            # cluster, but instead we ask the user to go through the full signup flow
            # to make sure they accept the privacy policy, and get appropraite tours
            user_email = ''

        set_user_field('static_user_id', static_user_id)
        set_user_field('user_email', user_email)

def set_user_field(field, value):
    """
    Updates the value of a specific field in user.json
    """
    with open(USER_JSON_PATH, 'r') as user_file_old:
        old_user_json = json.load(user_file_old)
        old_user_json[field] = value
        with open(USER_JSON_PATH, 'w+') as f:
            f.write(json.dumps(old_user_json))

def get_user_field(field):
    """
    Returns the value stored at field in the user.json file
    """
    try:
        with open(USER_JSON_PATH) as f:
            return json.load(f)[field]
    except: 
        return None
    
def get_static_user_id():
    return get_user_field('static_user_id')