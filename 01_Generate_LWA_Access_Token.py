#Description: This code is am example for obtaining an LWA Access Token through grant_type LWA Refersh Token

import sys,os
import requests  #Not a built-in Python library, you need to install it separately
import json
from urllib.parse import quote_plus, quote, urlencode

#The client_id, client_secret and LWA Refresh Token would come from the application you craete and self-authorize in Vendor Cenntral
client_id = ""
client_secret = ""
grant_type = "refresh_token"
refresh_token = ""

if client_id == '' or client_secret == '':
    print('No access keys')
    sys.exit()

base_url = "https://api.amazon.com/auth/O2/token?{}"

params = {"grant_type":grant_type,"client_id":client_id,"client_secret":client_secret,"refresh_token":refresh_token}
endpoint = base_url.format(urlencode(params, safe="()", quote_via=quote))

#********SEND the Request******
#request_url = endpoint + '?' + canonical_querystring
request_url = endpoint

print("\nBEGIN REQUEST+++++++++++++++++++++++++++++++++++++")
print("Request URL = "+ request_url)
r = requests.post(request_url)

print("\nRESPONSE++++++++++++++++++++++++++++++++++++++++++")
print('Response Code: %d\n' % r.status_code)

#********TO Pretty-print JSON*********
json_object = json.loads(r.text)
json_formatted_str = json.dumps(json_object, indent=2)

print(json_formatted_str)


