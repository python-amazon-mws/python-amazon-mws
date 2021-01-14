# Changelog

## v1.0dev16

*This update addresses these [issues](https://github.com/python-amazon-mws/python-amazon-mws/issues?q=milestone%3A1.0dev16+).*

This update focuses on the InboundShipments API, adding some new ways to input and manage data related to FBA shipments while also introducing some comprehensive documentation of the same.

Also includes the Products API's `get_my_fees_estimate` method, as well as deprecation warnings for old argument names to smooth the transition from v0.8.

### Changes

- **Products API `get_my_fees_estimate` method added.**
  - *See [#216](https://github.com/python-amazon-mws/python-amazon-mws/pull/216) for details.*
- **Deprecation warnings for old argument names.**
  - Some argument names for certain requests had changed between v0.8 and v1.0dev. This change makes it possible to use the v0.8 argument names in current code.
  - When using an old argument name, the method will raise a deprecation warning, indicating those old argument names will be removed in v1.1. The method will then proceed as expected using the correct arg names.
  - *See [#222](https://github.com/python-amazon-mws/python-amazon-mws/pull/222) for details.*
- **Datatype models added for InboundShipments.**
  - All models for this API can be found in `mws.models.inbound_shipments`.
  - Added datatype models for `Address`, `PrepDetails`, `InboundShipmentPlanRequestItem`, and `InboundShipmentItem`. These models can be used in relevant arguments for request methods related to FBA shipment creation and updating (`create_inbound_shipment_plan`, `create_inbound_shipment`, and `update_inbound_shipment`).
    - With this addition, it is now possible to include `PrepDetails` for items being added to shipments. This was not possible using the now-"legacy" item dictionary method (though it is still possible using the lower-level generic requests.)
  - Added `mws.models.inbound_shipments.shipment_items_from_plan` helper method.
    - The method can process the contents of a shipment plan from the parsed response from `create_inbound_shipment_plan`, turning the returned items into a set of `InboundShipmentItem` models automatically.
    - More details available in documentation
- **New documentation for Managing FBA Shipments added.**
  - Comprehensive documentation for how to manage FBA shipments using the InboundShipments API was added, titled **"Topics / Managing FBA Shipments"**.
  - This documentation showcases the usage of new models provided by this update, as well.

### Minor changes

- Links to Amazon MWS documentation throughout the code base updated from `http://` to `https://`.
- Type annotations added to methods for InboundShipments API.
  - As part of this, certain `assert`-style checks for argument types have been removed.
- Tests for InboundShipments request methods overhauled, removing dependency on `unittest` in favor of `pytest`.
- Slight URL naming changes for documentation, i.e. from "dotDict" to "DotDict".
  - Some bookmarks may break with this change, apologies!
- The Dev update callout removed from project README; will focus on the changelogs, instead.
- Development tooling configurations moved into `setup.cfg` for consistency.
- Project test suite expanded to Python 3.9 and Ubuntu-20.04
  - All automated testing is already performed in a matrix strategy, across Python 3.6, 3.7, 3.8, and 3.9; and on OSes Windows, MacOS, Ubuntu-18, and Ubuntu-20. Every combination of all these versions and OSes is tested.

## v1.0dev15

We're working on new features in the run-up to releasing v1.0. If you are using the latest `develop` branch version of the package, you can help us test these new features in your own environment.

### Changes

- **Dependencies have been updated: you may need to re-install requirements when upgrading.**
- **`DictWrapper` and `DataWrapper` are deprecated, and will be removed in v1.1.**
  - Starting in v1.0, `mws.response.MWSResponse` will be returned from all requests, instead.
- **`ObjectDict` and its alias `object_dict` are deprecated, and will be removed in v1.1.**
  - The `.parsed` interface of `DictWrapper` and `DataWrapper` is preserved in `MWSResponse`, but will return an instance of `mws.utils.collections.DotDict` instead of `ObjectDict`. `DotDict` is a more general-purpose object that subclasses `dict` and provides a similar interface, while still allowing keys to be accessed as attributes. New features of this object include the ability to assign values to existing keys, and any `dict` assigned to a key in a `DotDict` will automatically be wrapped in its own `DotDict` with no need for additional processing.
- **`XML2Dict` and its alias `xml2dict` are deprecated, and will be removed in v1.1.**
  - We will no longer perform XML parsing with our own methods. Instead, we are adding a dependency to `xmltodict`, which performs the same task a bit more cleanly.
  - Parsed content will no longer include superfluous extra dictionaries with `value` keys. *If your code looks for the `value` key, you may start seeing errors when testing new features.*
- **Generic requests added.**
  - *See PR #207 for details.*

### Testing new features.

**All features related to deprecations in v1.0dev15 are locked behind a feature flag**. Unless you explicitly set the feature flag as follows, your application *should* operate the same as before this update.

**If your application worked on a prior `develop` version and breaks when upgrading to v1.0dev15, please raise an issue so we may investigate.**

To enable and test the new features, first instantiate your API class as normal, then set `_use_feature_mwsresponse` to `True` on the API instance:

```python
from mws import Orders

api = Orders(...)
api._use_feature_mwsresponse = True

# Requests can be sent as normal:
response = api.list_orders()
# `response` should be an instance of `MWSResponse`,
# instead of the deprecated `DictWrapper` or `DataWrapper`.

# Use `.parsed` as before:
for order in response.parsed.Orders.Order:
    print(order.AmazonOrderId)
    # etc.
```

With this flag set, any request made through `api` will be wrapped in the new `MWSResponse` object; XML content will be parsed by the `xmltodict` dependency; and `response.parsed` will return a `DotDict` instance with your parsed data.

> **Note**: While `MWSResponse` maintains the same `.parsed` interface, other interfaces have changed compared to `DictWrapper` and `DataWrapper`. For instance, `DictWrapper.original` returned the *original bytes* of the response; whereas `MWSResponse.original` returns the *original `requests.Response` instance*. This provides better access to the full range of that response's data. So, to get the *bytes* content, you can use `MWSResponse.original.content`.

> Additionally, `MWSResponse` includes shortcut methods to some of the properties of `requests.Response`, including `.content`, `.text`, `.status_code`, `.headers`, etc. So, you can use `MWSResponse.content` as an equivalent to calling `MWSResponse.original.content`.

> More details are available in documentation: https://mws.readthedocs.io/en/develop/
