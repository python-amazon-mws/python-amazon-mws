"""Parameter manipulation utilities."""


def enumerate_param(param, values):
    """Builds a dictionary of an enumerated parameter, using the param string and some values.
    If values is not a list, tuple, or set, it will be coerced to a list
    with a single item.

    Example:
        enumerate_param('MarketplaceIdList.Id', (123, 345, 4343))
    Returns:
        {
            MarketplaceIdList.Id.1: 123,
            MarketplaceIdList.Id.2: 345,
            MarketplaceIdList.Id.3: 4343
        }
    """
    if not isinstance(values, (list, tuple, set)):
        # Coerces a single value to a list before continuing.
        values = [values]
    if not any(values):
        # if not values -> returns ValueError
        return {}
    if not param.endswith("."):
        # Ensure this enumerated param ends in '.'
        param += "."
    # Return final output: dict comprehension of the enumerated param and values.
    return {"{}{}".format(param, idx + 1): val for idx, val in enumerate(values)}


def enumerate_params(params=None):
    """For each param and values, runs enumerate_param,
    returning a flat dict of all results
    """
    if params is None or not isinstance(params, dict):
        return {}
    params_output = {}
    for param, values in params.items():
        params_output.update(enumerate_param(param, values))
    return params_output


def enumerate_keyed_param(param, values):
    """Given a param string and a dict of values, returns a flat dict of keyed, enumerated params.
    Each dict in the values list must pertain to a single item and its data points.

    Example:
        param = "InboundShipmentPlanRequestItems.member"
        values = [
            {'SellerSKU': 'Football2415',
            'Quantity': 3},
            {'SellerSKU': 'TeeballBall3251',
            'Quantity': 5},
            ...
        ]

    Returns:
        {
            'InboundShipmentPlanRequestItems.member.1.SellerSKU': 'Football2415',
            'InboundShipmentPlanRequestItems.member.1.Quantity': 3,
            'InboundShipmentPlanRequestItems.member.2.SellerSKU': 'TeeballBall3251',
            'InboundShipmentPlanRequestItems.member.2.Quantity': 5,
            ...
        }
    """
    if not isinstance(values, (list, tuple, set)):
        # If it's a single value, convert it to a list first
        values = [values]
    if not any(values):
        # Shortcut for empty values
        return {}
    if not param.endswith("."):
        # Ensure the enumerated param ends in '.'
        param += "."
    for val in values:
        # Every value in the list must be a dict.
        if not isinstance(val, dict):
            # Value is not a dict: can't work on it here.
            raise ValueError(
                (
                    "Non-dict value detected. "
                    "`values` must be a list, tuple, or set; containing only dicts."
                )
            )
    params = {}
    for idx, val_dict in enumerate(values):
        # Build the final output.
        params.update(
            {
                "{param}{idx}.{key}".format(param=param, idx=idx + 1, key=k): v
                for k, v in val_dict.items()
            }
        )
    return params


def dict_keyed_param(param, dict_from):
    """Given a param string and a dict, returns a flat dict of keyed params without enumerate.

    Example:
        param = "ShipmentRequestDetails.PackageDimensions"
        dict_from = {'Length': 5, 'Width': 5, 'Height': 5, 'Unit': 'inches'}

    Returns:
        {
            'ShipmentRequestDetails.PackageDimensions.Length': 5,
            'ShipmentRequestDetails.PackageDimensions.Width': 5,
            'ShipmentRequestDetails.PackageDimensions.Height': 5,
            'ShipmentRequestDetails.PackageDimensions.Unit': 'inches',
            ...
        }
    """
    params = {}

    if not param.endswith("."):
        # Ensure the enumerated param ends in '.'
        param += "."
    for k, v in dict_from.items():
        params.update({"{param}{key}".format(param=param, key=k): v})
    return params
