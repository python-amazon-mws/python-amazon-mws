############
Reports
############

Here is a very simple example of how to retrieve a report from Amazon
(assuming you already have a report ID from a different request, or from seller central)
using the python-amazon-mws wrapper.

.. code-block:: Python

    from mws import mws

    access_key = 'accesskey' #replace with your access key
    merchant_id = 'merchantid' #replace with your merchant id
    secret_key = 'secretkey' #replace with your secret key

    reportid = '123456' #replace with report id
  
    x = mws.Reports(access_key=access_key, secret_key=secret_key, account_id=merchant_id)
    report = x.get_report(report_id=reportid)
    response_data = report.original
    print response_data
