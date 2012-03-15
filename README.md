# Python Amazon MWS

Python Amazon MWS is a python interface for the Amazon MWS API.
I wrote it to help me upload my products to amazon. However, seeing its potential i decided
to expand it in order for it to cover most ( if not all ) operations in the Amazon MWS.

This is still an ongoing project. If you would like to contribute, see below :).


Its based on the [amazon-mws-python](http://code.google.com/p/amazon-mws-python).

# API usage

Make sure you check out the Amazon MWS documentation at https://developer.amazonservices.com/

Here's an exmaple of how to use python-amazon-mws to upload your products to amazon.


```python
from mws import mws

# You can get all these credentials when you sign up for Amazon MWS

MWS_ACCESS_KEY = 'your key'
MWS_SECRET_KEY = 'your secret'
MERCHANT_ID = 'your merchantid'

# Amazon supports different file formats for uploading products
# here i use a simple tsv file.

file_name = "templates/amazon-upload.tsv"

with open(file_name, "r+") as f:
    data = f.read()
    f.close()
    amazon = mws.Feeds(MWS_ACCESS_KEY, MWS_SECRET_KEY, MERCHANT_ID)
    response = amazon.submit_feed(data, feed_type="_POST_FLAT_FILE_LISTINGS_DATA_", 
                                    content_type="text/tab-separated-values;charset=iso-8859-1")

# In shell...

print response
<Element '{http://mws.amazonaws.com/doc/2009-01-01/}SubmitFeedResponse' at 0x8edaa4c>

```
For more information, check out the [Products API Documentation](https://developer.amazonservices.com/gp/mws/api.html/182-2079318-8524647?ie=UTF8&section=products&group=products&version=latest).

Here's another example in which i use python-amazon-mws to query amazon for a product using the product's UPC

```python
from mws import mws

MWS_ACCESS_KEY = 'your key'
MWS_SECRET_KEY = 'your secret'
MERCHANT_ID = 'your merchantid'
MARKETPLACE_ID = 'your marketplaceid'
UPC = "886039397430"

amazon = mws.Products(MWS_ACCESS_KEY, MWS_SECRET_KEY, MERCHANT_ID)
response = amazon.list_matching_products(UPC, MARKETPLACE_ID)

# In shell...

print response
<Element '{http://mws.amazonservices.com/schema/Products/2011-10-01}ListMatchingProductsResponse' at 0xa1b188c>

```

# Contribute

If you like the project, plz, contact me at commonzenpython@gmail.com (gtalk and email) and help me improve it.