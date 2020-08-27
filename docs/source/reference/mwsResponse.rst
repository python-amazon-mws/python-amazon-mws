MWSResponse
############

``MWSResponse`` acts as a wrapper for ``requests.Response`` objects returned from requests made to MWS.
When initialized, the response content is :ref:`automatically parsed for XML content <page_parsed_xml_responses>`,
making it available as a ``DotDict`` instance in :py:attr:`mws.response.MWSResponse.parsed`.

.. autoclass:: mws.response.MWSResponse
   :members:
   :inherited-members:

   .. attribute:: original
      :type: requests.Response

      Instance of the original ``requests.Response`` object. Can be used to get or set data in the
      original response.
