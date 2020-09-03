.. warning:: The following pertains to features added in **v1.0dev15** related to MWS requests.
   These features are disabled by default. To use these features, set flag ``_use_feature_mwsresponse`` to ``True``
   on an API class instance *before* making any requests:

   .. code-block:: python

      api_class = Orders(...)
      api_class._use_feature_mwsresponse = True

   If the flag is ``False``, all requests will return either ``DictWrapper`` or ``DataWrapper`` objects (deprecated);
   and parsed XML contents will be returned as an instance of ``ObjectDict`` (deprecated).

   *New features using* ``MWSResponse`` *and* ``DotDict`` *will become the default in v1.0.*
