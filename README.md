# Pyton Amazon MWS

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
For more information on feed uploading, check out the [Feeds API Documentation](https://developer.amazonservices.com/gp/mws/api.html/184-4424737-7926818?ie=UTF8&section=feeds&group=bde&version=latest).

# Contribute

If you like the project, plz, contact me at commonzenpython@gmail.com (gtalk and email) and help me improve it.