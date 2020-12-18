import os
from uuid import uuid4
from mws import Products
from mws.mws import Marketplaces
from mws.models.products import FeesEstimateRequest, PriceToEstimateFees, MoneyType

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


def get_fees():
    """
    Get amazon fees estimate for a single product
    """
    # Refer to the amazon documentation for this call as it links you through to the models used for
    # these calls for more information on what they expect.

    # Lets use the models already made in PythonAM
    # Refering to the signature for the .get_my_fees_estimate we need the following
    # price_to_estimate_fees requires a MoneyType for our price
    my_price = MoneyType(amount=123.45, currency_code="GBP")
    # This is a MoneyType for shipping which is passed into the price_to_estimate_fees for shipping
    my_shipping = MoneyType(amount=0.00, currency_code="GBP")
    # Combine the my_price and my_shipping into one PriceToEstimateFees object to send into the API call
    my_product_price = PriceToEstimateFees(listing_price=my_price, shipping=my_shipping)
    # Create a unique Id for this call (the uuid module is great for this)
    my_unique_identifier = str(uuid4())
    # Put it all together and send it off to amazon for their response.
    my_product = FeesEstimateRequest(
        Marketplaces.UK.marketplace_id,
        id_type="ASIN",
        id_value="B07QR73T66",
        price_to_estimate_fees=my_product_price,
        is_amazon_fulfilled=False,
        identifier=my_unique_identifier,
    )
    result = products_api.get_my_fees_estimate(my_product)
    print(result)


if __name__ == "__main__":
    ACCESS_KEY = os.environ["MWS_ACCESS_KEY"] if ACCESS_KEY is None else ACCESS_KEY
    SECRET_KEY = os.environ["MWS_SECRET_KEY"] if SECRET_KEY is None else SECRET_KEY
    ACCOUNT_ID = os.environ["MWS_ACCOUNT_ID"] if ACCOUNT_ID is None else ACCOUNT_ID
    products_api = Products(
        access_key=ACCESS_KEY, secret_key=SECRET_KEY, account_id=ACCOUNT_ID, region="UK"
    )
    # get fees for a single product
    get_fees()
