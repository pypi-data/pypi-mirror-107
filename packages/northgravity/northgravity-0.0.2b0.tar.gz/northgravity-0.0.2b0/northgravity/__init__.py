import os, sys
import logging


# Create the logger for the SDK
log = logging.Logger('NG SDK')
log.setLevel(logging.DEBUG)

# Save the logs into stdout - compatible with the Lambda's logging to the app
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# Set the logger
log.addHandler(handler)



# authentication process
TOKEN = os.getenv('NG_API_AUTHTOKEN')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')

# system env variables
JOB_ID = os.environ.get('JOBID')
PIPELINE_ID = os.environ.get('PIPELINE_ID')
EID = os.environ.get('EID')
ENDPOINT = os.environ.get('NG_API_ENDPOINT', 'https://api.northgravity.com')
COMPONENT_NAME = os.environ.get('NG_COMPONENT_NAME')
GROUP_NAME = os.environ.get('NG_STATUS_GROUP_NAME', '')


# Authentication from Token or login/password
if TOKEN is None or TOKEN == '':
    if LOGIN is None or LOGIN == '':
        raise Exception("No LOGIN found. Set the environment variable with the LOGIN")
    if PASSWORD is None or PASSWORD == '':
        raise Exception("No PASSWORD found. Set the environment variable with the PASSWORD")


# Import the methods
from .DatalakeHandler import *
from .TaskHandler import *
from .StatusHandler import *
from .Timeseries import *