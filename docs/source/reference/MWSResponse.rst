MWSResponse
############

.. versionadded:: 1.0dev15
   ``MWSResponse`` added

.. include:: /newFeaturesTopNote100dev15.rst

``MWSResponse`` acts as a wrapper for ``requests.Response`` objects returned from requests made to MWS.
When initialized, the response content is :doc:`automatically parsed for XML content <../topics/parsedXMLResponses>`,
making it available as a ``DotDict`` instance in :py:attr:`mws.response.MWSResponse.parsed`.

Parsed content for XML responses
================================

All XML response content is automatically parsed using the ``xmltodict`` package. The parsed results are stored as a
:py:class:`DotDict <mws.utils.collections.DotDict>` accessible from
:py:meth:`MWSResponse.parsed <mws.response.MWSResponse.parsed>`.

For more details on working with the parsed content, please see :doc:`DotDict`.

Original response access
========================

As ``MWSResponse`` wraps a ``requests.Response`` object, all data and methods of that underlying object can be accessed
from the ``MWSResponse`` instance using one of the following:

- The :py:attr:`MWSResponse.original <mws.response.MWSResponse.original>` attribute:

  .. code-block:: python

      response = api.foo_request(...)
      # response is an instance of MWSResponse

      response.original.status_code
      # 200
      response.original.headers
      # {'Content-Type': ...}

      response.original.text  # unicode
      # 'Hello world!'
      response.original.content  # bytes
      # b'Hello world!'

- A number of shortcut properties available on ``MWSResponse`` itself:

  .. code-block:: python

      response.content      # response.original.content
      response.cookies      # response.original.cookies
      response.elapsed      # response.original.elapsed
      response.encoding     # response.original.encoding
      response.headers      # response.original.headers
      response.reason       # response.original.reason
      response.request      # response.original.request
      response.status_code  # response.original.status_code
      response.text         # response.original.text

  Each of these shortcuts is a read-only property, with the exception of ``response.encoding``, which includes a
  setter for convenience when dealing with content encoding issues:

  .. code-block:: python

      response.encoding = "iso-8859-1"
      print(response.original.encoding)
      # "iso-8859-1"

MWSResponse API
===============

.. versionadded:: 1.0dev15
.. autoclass:: mws.response.MWSResponse
   :members:
   :inherited-members:

   .. attribute:: original
      :type: requests.Response

      Instance of the original ``requests.Response`` object. Can be used to get or set data in the
      original response.
