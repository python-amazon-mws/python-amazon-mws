import os
from uuid import uuid4

from mws import Products
from mws.models.products import FeesEstimateRequest, MoneyType, PriceToEstimateFees
from mws.mws import Marketplaces

# You can add your credentials here if you don't want to use environment variables
ACCESS_KEY = None
SECRET_KEY = None
ACCOUNT_ID = None


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
