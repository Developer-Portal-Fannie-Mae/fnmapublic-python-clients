import client_nonpaginated_api
from client_nonpaginated_api import do_get
import client
from client import smart_open
import json
import sys
 

def log(msg):
		sys.stderr.write(msg + "\n")

def run_nhs(api_uri, output_name=None):
	base_uri = "https://api.fanniemae.com"
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
		raw_string = json.dumps(response.json(),indent=2).replace('.0','')
		output_file.write(raw_string)
	return output_file_name
	   
'''Our main function -- only gets invoked if this is the "outer"
   Python script invoked.
   Thanks to Tierney Pitzer for this if statement.'''
if __name__ == "__main__":  
	if len(sys.argv) > 1:
		output_file_name = sys.argv[1]
	else:
		output_file_name = "-"

	log("writing output to " + output_file_name)
	NHS_API = "/v1/nhs/results"
	output_file_name = run_nhs(NHS_API,output_file_name)
