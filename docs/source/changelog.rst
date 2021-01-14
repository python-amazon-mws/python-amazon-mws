CHANGELOG
#########

v1.0dev16
=========

.. note:: This is a **prerelease** version for **v1.0**.

:Date: November 2020
:Issues: `See here <https://github.com/python-amazon-mws/python-amazon-mws/issues?q=milestone%3A1.0dev16+>`_

This update focused on the InboundShipments API, adding some new ways to input and manage data related to FBA shipments
while also introducing some comprehensive documentation of the same.

Also includes the Products API's `get_my_fees_estimate` method, deprecation warnings for old argument names to smooth
the transition from v0.8.

.. _v1-0-dev-16-major-changes:

Major changes
-------------

- Products API :py:meth:`get_my_fees_estimate <mws.apis.products.Products.get_my_fees_estimate>` method added.

  - See `#216 <https://github.com/python-amazon-mws/python-amazon-mws/pull/216>`_ for details.

- Deprecation warnings for old argument names.

  - Some argument names for certain requests had changed between v0.8 and v1.0dev.
    This change makes it possible to use the v0.8 argument names in current code.
  - When using an old argument name, the method will raise a deprecation warning, indicating those old argument names
    will be removed in v1.1. The method will then proceed as expected using the correct arg names.
  - See `#222 <https://github.com/python-amazon-mws/python-amazon-mws/pull/222>`_ for details.

- Datatype models added for InboundShipments.

  - All models for this API can be found in module ``mws.models.inbound_shipments``.
  - Added datatype models for :py:class:`Address <mws.models.inbound_shipments.Address>`,
    :py:class:`PrepDetails <mws.models.inbound_shipments.PrepDetails`,
    :py:class:`InboundShipmentPlanRequestItem <mws.models.inbound_shipments.InboundShipmentPlanRequestItem`, and
    :py:class:`InboundShipmentItem <mws.models.inbound_shipments.InboundShipmentItem`.
    These models can be used in relevant arguments for request methods related to FBA shipment creation and updating
    (:py:meth:`create_inbound_shipment_plan <mws.apis.inbound_shipments.InboundShipments.create_inbound_shipment_plan>`,
    :py:meth:`create_inbound_shipment <mws.apis.inbound_shipments.InboundShipments.create_inbound_shipment>`, and
    :py:meth:`update_inbound_shipment <mws.apis.inbound_shipments.InboundShipments.update_inbound_shipment>`.

    - With this addition, it is now possible to include
      :py:class:`PrepDetails <mws.models.inbound_shipments.PrepDetails>` for items being added to shipments.
      This was not possible using the now-"legacy" item dictionary method (though it is still possible using the
      lower-level generic requests).

  - Added :py:func:`shipment_items_from_plan <mws.models.inbound_shipments.shipment_items_from_plan>` helper method.

    - The method can process the contents of a shipment plan from the parsed response from
      ``create_inbound_shipment_plan``, turning the returned items into a set of ``InboundShipmentItem`` models
      automatically.

- **New documentation for Managing FBA Shipments added.**

  - See: :doc:`topics/managingFBAShipments`.
  - Comprehensive documentation for how to manage FBA shipments using the InboundShipments API.
  - Showcases the usage of new models provided by this update.

.. _v1-0-dev-16-minor-changes:

Minor changes
-------------

- Links to Amazon MWS documentation throughout the code base updated from `http://` to `https://`.
- Type annotations added to request methods for InboundShipments API.
  - As part of this, certain `assert`-style checks for argument types have been removed.
- Tests for InboundShipments request methods overhauled, removing dependency on `unittest` in favor of `pytest`.
- URL naming improvements for documentation pages, and proper usage of doc links instead of adding extraneous anchor links.
  - Some bookmarks may break with this change, apologies!
- Dev update callout removed from project README.
- Development tooling configurations moved into `setup.cfg` for consistency.
- Project test suite expanded to Python 3.9 and Ubuntu-20.04
  - All automated testing is already performed in a matrix strategy, across Python 3.6, 3.7, 3.8, and 3.9; and on OSes Windows, MacOS, Ubuntu-18, and Ubuntu-20. Every combination of all these versions and OSes is tested.

v1.0dev15
=========

.. note:: This is a **prerelease** version for **v1.0**.

:Date: September 2020

This update represents a major step towards a v1.0 release candidate. Much of the core components of the project
have been restructured, new XML parsing logic has been added, and API code has been streamlined to ease development
efforts going forward.

.. _v1-0-dev-15-major-changes:

Major changes
-------------

- Added dependency ``xmltodict`` for parsing XML documents to Python dict objects.
- Added ``MWSResponse``, intended to replace ``DictWrapper`` and ``DataWrapper`` response wrappers; and
  ``DotDict``, intended to replace ``ObjectDict``.

  - These features are in preview mode. See [#f1]_ .

- Added ``MWS.generic_request()``, a low-level interface for sending requests to any MWS operation
  with any set of parameters necessary (using new utility function, ``mws.utils.params.flat_dict_param``).
- Several objects have been moved, renamed, and/or retooled to improve code structuring and interoperability, most
  notably ``mws.utils`` (which has been broken down to multiple modules with different concerns).

.. _v1-0-dev-15-code-restructuring:

Code restructuring
------------------

Several objects have been moved and/or renamed, with new modules added to contain them. At the same time,
the namespace for most of those objects has been left mostly intact. Following changes relate to objects whose
imports may need to be adjusted in application code.

- ``mws.utils``, formerly a single module file, is now a directory containing other modules with separated concerns.
- Moved ``mws.mws.DictWrapper`` to ``mws.utils.DictWrapper``.
- Moved ``mws.mws.DataWrapper`` to ``mws.utils.DataWrapper``.
- Moved ``mws.mws.ObjectDict`` to ``mws.utils.ObjectDict``.
- Moved ``mws.mws.XML2Dict`` to ``mws.utils.XML2Dict``.
- Moved/renamed ``mws.mws.clean_params`` to ``mws.utils.clean_params_dict``.

  - "Cleaning" logic has been broken down further with ``mws.utils.params.clean_value``, which passes to other
    "clean_FOO" methods such as ``clean_string``, ``clean_bool``, and ``clean_date``.

- Changed ``mws.utils.get_utc_timestamp`` to ``mws.utils.mws_utc_now``.

  - ``get_utc_timestamp`` returned an ISO-8601-formatted string of the current datetime in UTC timezone.
    ``mws_utc_now`` produces the same datetime, but instead returns a ``datetime.datetime`` object.
    An ISO-8601 formatted string can easily be obtained using the ``.isoformat()`` method.

- Changed ``mws.mws.remove_namespace`` to ``mws.utils.remove_xml_namespaces``.

  - The new version works the same as the old, but can now accept bytes as well as strings.

.. _v1-0-dev-15-deprecations:

Deprecations
------------

The following have been **deprecated**:

- ``DictWrapper`` (removed in v1.1), replaced by ``MWSResponse`` in v1.0 (currently in preview mode).
- ``DataWrapper`` (removed in v1.1), replaced by ``MWSResponse`` in v1.0 (currently in preview mode).
- ``ObjectDict`` (removed in v1.1), replaced by ``DotDict`` in v1.0 (currently in preview mode).
- ``XML2Dict`` (removed in v1.1). XML parsing into Python objects will be performed by the ``xmltodict`` library
  starting in v1.0.
- ``MWS.enumerate_param`` (removed in v1.0). Use utility methods found in ``mws.utils.params``, instead.

.. _v1-0-dev-15-minor-changes:

Minor changes
-------------

- New arguments are available when instantiating an API class (subclasses of the ``MWS`` main class, such as
  ``Feeds`` and ``Orders``):

  - Argument and class attr ``user_agent_str`` sets the User Agent String sent with requests to MWS. This can be used
    to override PAM's default agent string, ``"python-amazon-mws/{version} (Language=Python)"``.
  - Argument ``headers`` and attribute ``extra_headers`` accepts a dictionary with headers to add to each request,
    if necessary. Headers can still be altered per-request by passing an ``extra_headers`` kwarg to ``make_request``
    or ``generic_request``.
  - Argument and class attr ``force_response_encoding`` allows specifying the encoding used to decode a response's
    bytes content, when parsed by ``MWSResponse`` into a ``DotDict``.

    - Amazon documentation states they use ISO-8859-1 (aka Latin-1) encoding. However, some responses may still be
      encoded differently, such as in UTF-8, even if this behaviour is not well-documented. By default,
      python-amazon-mws relies on ``requests.Response.apparent_encoding`` to guess the character set to decode,
      which should be sufficient for most uses.
    - Setting ``force_response_encoding='utf-8'``, for example, will force responses to be decoded as UTF-8
      automatically for any request made with that API class instance.
    - Encoding can also be adjusted on the ``MWSResponse`` object, by assigning ``response.encoding = 'utf-8'``
      and then calling ``response.parse_response()`` to re-parse content.

- All request methods are now required to pass the ``Action`` name of an MWS operation as the first argument to
  ``MWS.make_request`` or ``MWS.generic_request``. Previously, this was expected as a parameter in the data sent with
  a request.
- ``MWS.make_request`` argument ``extra_data`` has been renamed to ``params``, and can now default to ``None``.
  This permits operations such as ``GetServiceStatus``, which require no parameters, to pass without issue.
- The ``timeout`` kwarg in ``MWS.make_request`` has been promoted to a named argument, with a default value of
  300 seconds.

.. rubric:: Footnotes

.. [#f1] **1.0dev15 features preview**: Prior to **v1.0**, ``DictWrapper`` and ``DataWrapper`` will still be used
   as default response wrappers for all requests; and the ``.parsed`` interface for these objects will continue to be
   ``ObjectDict`` instances.

   To use ``MWSResponse`` and ``DotDict`` for response parsing in development versions (1.0dev15 and up),
   you must enable the ``_use_feature_mwsresponse`` feature flag:

   1. Instantiate an API class, i.e. ``feeds_api = Feeds(...)``.
   2. Set flag ``_use_feature_mwsresponse`` to ``True`` on the class instance:
      ``feeds_api._use_feature_mwsresponse = True``.

   Now all requests made through this class instance will return responses as ``MWSResponse``.
