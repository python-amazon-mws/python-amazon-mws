# Changelog

## v1.0dev16

*TODO*

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
