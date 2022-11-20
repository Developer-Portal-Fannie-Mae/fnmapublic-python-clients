import base64
import hmac
import hashlib
import json
import os
import sys
import contextlib
import requests
import ssl
from requests.auth import HTTPBasicAuth


'''primary public entrypoint to this module --
   given a valid client.properties file located in
   $CLIENT_HOME (or %%CLIENT_HOME%% if you are
   a command-prompt person), this function returns a valid
   Authorization Token that can be used to make FNMA Public API calls. '''
def get_auth_token():
    client_properties = load_properties()
    secret_str = client_properties["client-secret"]
    secret_bytes = to_byte_array(secret_str)
    client_id_str = client_properties["client-id"]
    return ping_auth(secret_str, client_id_str)

''' Load client properties from
    $CLIENT_HOME/client.properties.'''
def load_properties():
    #get the client home directory name or die trying
    home_directory_name = os.environ.get('CLIENT_HOME')
    if home_directory_name == None:
        user_home = os.environ.get('USERPROFILE')
        if user_home == None:
            raise Exception("neither CLIENT_HOME nor USERPROFILE defined, cannot read client properties and therefore cannot proceed")
        home_directory_name = user_home + "/fnmapublic-python-clients-master/pythonClient/dpPublic"
    properties_file_name = "client.properties"
    properties_file_path = home_directory_name + "/" + properties_file_name
    print(home_directory_name)
    #open and load the contents of client.properties, or die trying
    with open(properties_file_path) as propFile:
        return json.load(propFile)


''' Convenience function to convert a string to a byte array. '''
def to_byte_array(string_value):
    new_bytes = bytearray()
    new_bytes.extend(string_value.encode())
    return new_bytes

'''Given a PingOne client ID and client secret known
   to the designated client, authenicate the user and return an
   authorization token.  '''
def ping_auth(secret_str, client_id_str):
    accessTokenUrl = 'https://auth.pingone.com/4c2b23f9-52b1-4f8f-aa1f-1d477590770c/as/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    basic = HTTPBasicAuth(client_id_str, secret_str)
    payload = {'grant_type': 'client_credentials'}
    pingresponse = requests.post(accessTokenUrl, verify='zsPublicCert.pem', auth=basic,
                                    data=payload).json()
    return pingresponse

'''Generate an HMAC256 key to pass to cognito'''
def getHmac(secret_bytes, msg_bytes):
    dig = hmac.new(secret_bytes, msg_bytes, digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()      


'''A simple helper to generate a temp file name.
   The file name will be ${tmpDir}/prefix${PID}suffix'''
def tmpFileName(prefix, suffix, tmpDir=''):
    if tmpDir == '':
        if not 'TMP' in os.environ:
            raise Exception("no temp directory specified as $TMP or %%TMP%%")
        tmpDir=os.environ['TMP']
    return tmpDir+"/"+prefix+ str(os.getpid()) + suffix

'''Thanks to https://stackoverflow.com/a/17603000/3839108 for this function.
   This function allows us to open either a named file or stdout in the
   context of a with block.'''
@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

'''If run directly from this module (as opposed to this module being imported
   into another module), then the following lines are executed; this is
   basically our equivalent of a java public static void main '''
if __name__ == "__main__":
    cognito_response = get_auth_token()
    id_token = cognito_response['access_token']
    with smart_open('-') as output:
        output.write(id_token)

