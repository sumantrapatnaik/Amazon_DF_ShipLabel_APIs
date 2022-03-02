# Amazon_DF_ShipLabel_APIs
This repo has sample Python code for calling Amazon DF Shipping Label APIs with a custom coded AWS Signature4 generation 

Dependencies and References:

1.All the libraries being used in the smaple code are built-in Python libraries except the 'requests' library. Reference link 1: to install 'requests' library: https://pypi.org/project/requests/

2a.CODE REFERENCE 1: https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html

2b.CODE REFERENCE 2: https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html



The following is a description of each of the Python files:

a. 1_Generate_LWA_Access_Token.py : This has the code to call the Auth endpoint "https://api.amazon.com/auth/o2/token" to retrieve an LWA Access Token by providing the client ID, client secret and LWA Refresh Token of your application. These values would come from the application that you create and then self-authorize in Amazon Vendor Central

b. 2_Generate_RDT.py : This has the code to call the enpoint "https://sellingpartnerapi-na.amazon.com/tokens/2021-03-01/restrictedDataToken" to retrieve the Restricted Data Token by providing the AWS Acces Key, AWS Secret Key (would come the AWS User) and LWA Access Token (retieved in the earlier API call)

c. 3_POST_Submit_Shipping_Label.py : This has sample code to call the endpoint "https://sellingpartnerapi-na.amazon.com/vendor/directFulfillment/shipping/v1/shippingLabels" to siubmit a Shipping Label generation request for an order or a batch of orders. The code generates an LWA Access Token and then uses it to POST call the "sellingpartnerapi-na" endpoint.

d. 4_GET_Transaction_Status.py : This has sample code to call the endpoint "https://sellingpartnerapi-na.amazon.com/vendor/directFulfillment/transactions/v1/transactions" to check the Transaction Status of the transaction ID received in reponse of the above POST Submit Shipping Label call. Note that this API call is oprtional. The code generates an LWA Access Token and then uses it to GET call the "sellingpartnerapi-na" endpoint.

e. 5a_GET_Shipping_Labels_with_RDT.py: This has sample code to call the endpoint "https://sellingpartnerapi-na.amazon.com/vendor/directFulfillment/shipping/v1/shippingLabels" to reterieve or get the Shipping Labels generated withing a time window, by passing the createdAfter, createdBefore datetime, and limit as Query String parameters. Note that the Query String Parameters are used in the AWS Signature4 generation function as well. The code generates an LWA Access Token and then uses it to geenrate an RDT and then uses the RDT to GET call the "sellingpartnerapi-na" endpoint.

f. 5b_GET_Shipping_Label_with_RDT_PerOrder.py: This has sample code to call the endpoint "https://sellingpartnerapi-na.amazon.com/vendor/directFulfillment/shipping/v1/shippingLabels" to reterieve or get the Shipping Labels generated for one order by passing the order number in the endpoint URL. The code generates an LWA Access Token and then uses it to geenrate an RDT and then uses the RDT to GET call the "sellingpartnerapi-na" endpoint.

