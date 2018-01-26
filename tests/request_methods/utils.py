"""
Utilities common to request method tests.
"""


def clean_redundant_params(params):
    """
    Removes commonly-expected or hard-to-guess keys from the params,
    such as Timestamp (generated by make_request), account details, and signature params.
    """
    del params['AWSAccessKeyId']
    del params['SellerId']
    del params['SignatureMethod']
    del params['SignatureVersion']
    del params['Timestamp']
    return params
