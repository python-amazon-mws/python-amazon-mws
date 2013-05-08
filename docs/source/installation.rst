Installation
=============
This process assumes you have already created an Amazon Marketplace Webservices (MWS) account.

Setup API Access
---------------------

* Go to https://developer.amazonservices.com (or .ca/.de/.jp/.fr/.co.uk)
* Click on the *Sign up for MWS* button and follow the instructions.
* At the end you must have a screen (print it and save it !)
	This screen will contain the following credentials:
		* Merchant Id (or Seller Id) - This is your unique merchant/seller ID
		* Marketplace Id - This is the id for the marketplace you are selling on.
						    It allows you to target specific markerplaces (US, Japan, Europe, etc..) in which you are authorized to sell.
		* Access key - Used to identify the user of this API.
		* Secret key - This is used to authenticate every request sent to Amazon
	Make sure to keep this confidential as these credentials can potentially compromise your account.


Test API Access
-----------------

* Go to https://mws.amazonservices.com/scratchpad/index.html (you can change the domain .com like before)
* In API selection, choose **Products** and *ListMatchingProducts*
* In Authentication put your credentials.
* Input the desired MarketplaceId and put "python" in Query
* Click on the submit button

If everything is good, you can see a response 200 and a list of item matching python


Install MWS Python API :)
-------------------------

From PyPi

.. code-block:: bash

    $ pip install python-amazon-mws

