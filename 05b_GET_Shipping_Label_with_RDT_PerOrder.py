#Description: This code is am example for generating the AWS Signature V4 and use it to call DF SP API GET Shipping Label for an order using RDT
#CODE REFERENCE: https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
#Reference link 1: to install 'requests' library: https://pypi.org/project/requests/
#Reference Link 2: https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html

import sys,os,datetime,hmac,hashlib
import requests   #Not a built-in Python library, you need to install it separately
import json, urllib.parse
from urllib.parse import quote_plus, quote, urlencode


def sign(key,msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

def uriEncode(param):
    return urllib.parse.quote(param, safe='')

def generateAuthHeaders(method, service, host, region, f_canonical_uri, f_canonical_querystring, raw_payload, access_key, secret_key, access_token):
    
    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d')

    #******TASK-1 : Create a Canonical Request********
    if method == 'POST':
        payload_hash = hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()
    elif method == 'GET':
        payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()

    #canonical_uri is the URI-encoded version of the absolute path component of the URI—everything starting with the "/" that follows the domain name and up to the end of the string or to the question mark character ('?') if you have query string parameters 
    canonical_uri = f_canonical_uri 

    #Canonical_querystring is the the URI-encoded query string parameters. URI-encode name and values individually. You must also sort the parameters in the canonical query string alphabetically by key name. 
    #The sorting occurs after encoding
    #Even if there are no Query Pararmeters in the URL, an empty string needs to be there in the canonical_request
    canonical_querystring = f_canonical_querystring  

    #Create the canonical headers and signed headers. Header names must be trimmed and lowercase, and sorted in code point order from low to high. Note that there is a trailing \n.
    canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
    signed_headers = 'host;x-amz-date'  #Add the headers based on the API call in the same sequence as canonical_headers

    canonical_request = method + '\n' + canonical_uri +'\n'+ canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

    #print("TASK 1 Canonical_request =", canonical_request)

    #******TASK-2 : Create the String to Sign********
    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
    string_to_sign = algorithm + '\n' + amzdate + '\n' + credential_scope + '\n' + hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

    #print ('TASK 2 String-to-Sign=',string_to_sign)

    #******TASK-3 : Calculate the Signature**********
    signing_key = getSignatureKey(secret_key, datestamp, region, service)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    #print ('TASK 3 Signature =', signature)

    #*******TASK 4 : Add Signing Information to the Request********
    authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' + 'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    #These are the Headers that must be there in your HTTP request
    if method == 'POST':
        l_headers = {'Authorization':authorization_header, 'x-amz-access-token':access_token,'x-amz-content-sha256':payload_hash,'x-amz-date':amzdate}
    elif method == 'GET':
        l_headers = {'Authorization':authorization_header, 'x-amz-access-token':access_token,'x-amz-date':amzdate}

    return l_headers

#BEGIN*************To Generate LWA Access Token****************
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

if r.status_code == 200 and json_formatted_str != "":
    r_access_token = json_object["access_token"]
else:
    r_access_token = ""

#END*************To Generate LWA Access Token****************

#BEGIN*************To Generate RDT****************

#AWS Access Key and AWS Secret Access Key from the AWS User needs to be used here
access_key = ''
secret_key = ''

#Use the LWA Access Token received above in the API call
access_token = r_access_token

#For calling RDT Generation Endpoint
method = 'POST'
service = 'execute-api'
host = 'sellingpartnerapi-na.amazon.com'
region = 'us-east-1'
endpoint = 'https://sellingpartnerapi-na.amazon.com/tokens/2021-03-01/restrictedDataToken'

raw_payload ='{'
raw_payload += '"restrictedResources":'
raw_payload += '['
raw_payload += '{"method": "GET",'
raw_payload += '"path": "/vendor/directFulfillment/shipping/v1/shippingLabels"'
raw_payload +='}'
raw_payload +=','
raw_payload += '{"method": "GET",'
raw_payload += '"path": "/vendor/directFulfillment/shipping/v1/shippingLabels/{litun}"'    #{something} this value can be any string
raw_payload +='}'
raw_payload +=']'
raw_payload +='}'

canonical_uri = "/tokens/2021-03-01/restrictedDataToken"
canonical_querystring = ""

if access_key == '' or secret_key == '':
    print('No access keys')
    sys.exit()

headers = generateAuthHeaders(method,service,host,region,canonical_uri,canonical_querystring,raw_payload,access_key,secret_key,access_token)

#********SEND the Request to generate RDT******
request_url = endpoint

print("\nBEGIN REQUEST+++++++++++++++++++++++++++++++++++++")
print("Request URL = "+ request_url)
r = requests.post(request_url, data=raw_payload, headers=headers)

print("\nRESPONSE++++++++++++++++++++++++++++++++++++++++++")
print('Response Code: %d\n' % r.status_code)

#********TO Pretty-print JSON*********
json_object = json.loads(r.text)
json_formatted_str = json.dumps(json_object, indent=2)

print(json_formatted_str)

if r.status_code == 200 and json_formatted_str != "":
    rdt_val = json_object["restrictedDataToken"]
else:
    rdt_val = ""

#print(rdt_val)
#END*************To Generate RDT****************

#BEGIN***********For calling GET Shipping Label*****************
method = 'GET'
service = 'execute-api'
host = 'sellingpartnerapi-na.amazon.com'
region = 'us-east-1'
endpoint = 'https://sellingpartnerapi-na.amazon.com/vendor/directFulfillment/shipping/v1/shippingLabels'

#LWA Access Token will be the RDT received in earlier API call
access_token = rdt_val

#Put the value of the Order Number
order_number = ""

#No payload in a GET call
raw_payload = ""

#canonical_uri is the URI-encoded version of the absolute path component of the URI—everything starting with the "/" that follows the domain name and up to the end of the string or to the question mark character ('?') if you have query string parameters 
canonical_uri = "/vendor/directFulfillment/shipping/v1/shippingLabels"+ "/" + order_number

#canonical_querystring is the the URI-encoded query string parameters. URI-encode name and values individually. 
canonical_querystring = "" #will be an empty string in case there are no Query String Parameters

headers = generateAuthHeaders(method,service,host,region,canonical_uri,canonical_querystring,raw_payload,access_key,secret_key,access_token)

request_url = endpoint + '/' + order_number
#request_url = endpoint

print("\nBEGIN REQUEST+++++++++++++++++++++++++++++++++++++")
print("Request URL = "+ request_url)
r = requests.get(request_url, headers=headers)

print("\nRESPONSE++++++++++++++++++++++++++++++++++++++++++")
print('Response Code: %d\n' % r.status_code)

#********TO Pretty-print JSON*********
json_object = json.loads(r.text)
json_formatted_str = json.dumps(json_object, indent=2)

print(json_formatted_str)

#END***********For calling GET Shipping Label*****************
