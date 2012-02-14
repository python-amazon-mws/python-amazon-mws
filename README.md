# Pyton Amazon MWS

Pyton Amazon MWS is a python interface for the Amazon MWS API.
I created wrote to help me upload my products to amazon. However, seeing its potential i decided
to expand it in order for it to cover most ( if not all ) operations in the Amazon MWS.


Its based on the [amazon-mws-python](http://code.google.com/p/amazon-mws-python).

# Basic usage

Say i want to get the ASIN for a certain product and all i have is its UPC

Import the api class ( same as amazon api ). 
In this case i am going to use the Products API.

```python
from mws import mws

MWS_ACCESS_KEY = 'your key'
MWS_SECRET_KEY = 'your secret'
MERCHANTID = 'your merchantid'
MARKETPLACEID = 'your marketplace id'

# You can get all the above credentials when you sign up for Amazon MWS

amazon = mws.Feeds(MWS_ACCESS_KEY, MWS_SECRET_KEY, MERCHANTID)
response = amazon.submit_feed(data, feed_type="_POST_FLAT_FILE_LISTINGS_DATA_", 
                                    content_type="text/tab-separated-values;charset=iso-8859-1")
                                    
# For more information on the above parameters, check out the Feeds API Documentation


UPC = "885259292327"
amazon = mws.Products(MWS_ACCESS_KEY, MWS_SECRET_KEY, MERCHANTID)
response = amazon.list_matching_products("", MARKETPLACEID) 

```
### Important (and basic) things!

Make sure you check out the Amazon MWS documentation at https://developer.amazonservices.com/

# Contribute

If you like the project, plz, contact me at commonzenpython@gmail.com (gtalk and email) and help me improve it.