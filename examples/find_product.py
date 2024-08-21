import os

from mws import Products
from mws.mws import Marketplaces

# You can add your credentials here if you don't want to use environment variables
ACCESS_KEY = None
SECRET_KEY = None
ACCOUNT_ID = None


def find_asin(amazon_type="ASIN", product="B07QR73T66"):
    """
    Find a specific product by ASIN - note the use of a list here.

    We are setting some defaults for the amazon_type and product here, they are ASIN and the
    relevant ASIN for a focusrite saffire audio interface

    """

    # Make sure we send a LIST of ids in.
    if not isinstance(product, list):
        product = [product]

    # Call the products api and get find products in amazons catalogue based on our query parameters.
    # Notice how we are using our Marketplaces enum to send in the correct marketplace ID
    results = products_api.get_matching_product_for_id(
        marketplace_id=Marketplaces.UK.marketplace_id, type_=amazon_type, ids=product
    )

    print(
        "ORIGINAL XML RESPONSE - \
        use this for debugging or raising issues with - check for confidential information first."
    )
    print(results.original)

    print("The dict like (ObjectDict) response")
    print(results.parsed)

    # the .parsed node is not guaranteed to be a list so convert it if not.
    if not isinstance(results.parsed, list):
        found_products = [results.parsed]
    else:
        found_products = results.parsed

    # Output some useful data showing dot notation of the ObjectDict.
    for example in found_products:
        print("The product title")
        print(example.Products.Product.AttributeSets.ItemAttributes.Title)
        print("The category")
        print(example.Products.Product.SalesRankings.SalesRank[0].ProductCategoryId)
        print("The current sales rank")
        print(example.Products.Product.SalesRankings.SalesRank[0].Rank)


if __name__ == "__main__":
    ACCESS_KEY = os.environ["MWS_ACCESS_KEY"] if ACCESS_KEY is None else ACCESS_KEY
    SECRET_KEY = os.environ["MWS_SECRET_KEY"] if SECRET_KEY is None else SECRET_KEY
    ACCOUNT_ID = os.environ["MWS_ACCOUNT_ID"] if ACCOUNT_ID is None else ACCOUNT_ID
    products_api = Products(
        access_key=ACCESS_KEY, secret_key=SECRET_KEY, account_id=ACCOUNT_ID, region="UK"
    )
    # Find product details via Amazon ASIN
    find_asin(amazon_type="ASIN", product="B07QR73T66")
    # Find product details via EAN code - note sending this in as a string and also multiple id's
    find_asin(amazon_type="EAN", product=["0815301005230", "5060374260160"])
