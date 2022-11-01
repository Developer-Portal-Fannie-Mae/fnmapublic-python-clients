import requests
import sys
import client
from client import smart_open
import json
import os
import tempfile


'''Make a request to an eXchange non-paginated API.
   @Param api_uri String -- API's URI (does not include the "base" URI)
   @Param data_set_type String -- name of the data set type that is fetched via the request
   @Param output_name (optional) -- name of file in which to place output; if None then a file name is generated
   @Return string -- name of output file
'''
def run(api_uri, output_name=None):
    base_uri = "https://api-devl-int.intgfanniemae.com"
    #use the exchange_client to get our access token
    full_auth = client.get_auth_token()
    user_token = full_auth['access_token']
    uri = base_uri + api_uri
    if output_name is None:
        output_file_name = '-'
    else:
        output_file_name = output_name
    with smart_open(output_file_name) as output_file:
        response = do_get(uri,user_token)
        json.dump(response.json(),output_file,indent=2)
    return output_file_name
'''---------------------------------------------------------------------------'''

'''Request content from uri, return as a response object.'''
def do_get(uri, user_token):
    r = requests.get(uri,headers={"x-public-access-token": user_token, "Accept": "application/json"}, verify='C:/Users/r2ua5m/fnmaroot.pem')
    if r.status_code != 200:
        raise Exception(uri + " resulted in an HTTP " + str(page_num))
    return r
