============
Installation
============

This process assumes you have already created an Amazon Marketplace Web Service (MWS) account.

-----------------
Set up API Access
-----------------

- Visit https://developer.amazonservices.com.

.. seealso:: Different developer portals are available for different regions.
   See a list of regional portal pages in Amazon MWS documentation,
   `Related Resources <http://docs.developer.amazonservices.com/en_US/dev_guide/DG_Resources.html>`_.

- Click **Register as a developer**.
- Sign in to your Amazon Professional Seller account, then follow the instructions.
- At the end of the process, you will be presented with a set of **credentials**, including:

  - **Merchant ID** (or **Seller ID**) - This is your unique merchant/seller ID
  - **Marketplace ID** - This is the ID for the marketplace you are selling on.
    This allows you to target specific marketplaces (US, Japan, Europe, etc..)
    in which you are authorized to sell.
  - **Access key** - Used to identify the user of this API.
  - **Secret key** - This is used to authenticate every request sent to Amazon

Print, save, or otherwise securely store the credentials for your account.
You will need them in order to send requests to MWS.

.. warning:: These credentials can be used to compromise your account, change product listings,
   make shipments, cancel orders, and so on; similar to having direct access to your
   Seller Central account.

   You should keep these credentials confidential at all times
   (i.e. never commit them to version control!).

---------------------
Test using Scratchpad
---------------------

- Open the `MWS Scratchpad <https://mws.amazonservices.com/scratchpad/>`_
- In API selection, choose **Products** and *ListMatchingProducts*
- Add your credentials to the **Authentication** section.
- Input the desired MarketplaceId and put "python" in Query
- Click **Submit**.

If everything is good, you can see a response 200 and a list of item matching python

.. seealso:: For more info on using the MWS scratchpad, see Amazon's documentation:
   `Using Amazon MWS Scratchpad <http://docs.developer.amazonservices.com/en_US/scratchpad/Scratchpad_Using.html>`_

-----------------------------
Install ``python-amazon-mws``
-----------------------------

#########
From PyPi
#########

Install **0.8.x** version using ``pip``:

.. code-block:: bash

    $ pip install mws

.. note:: The latest **1.0.0dev** version is *not* currently available on PyPI.

###########
From Github
###########

Install **0.8.x** version from the ``master`` branch using ``pip``:

.. code-block:: bash

    $ pip install git+https://github.com/python-amazon-mws/python-amazon-mws.git@master#egg=mws

You can also install the latest **1.0.0dev** version from ``develop`` branch:

.. code-block:: bash

    $ pip install git+https://github.com/python-amazon-mws/python-amazon-mws.git@develp#egg=mws
