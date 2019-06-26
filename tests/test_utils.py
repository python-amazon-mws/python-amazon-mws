from mws.mws import calc_request_description
from mws.utils import calc_md5, xml2dict


def test_calc_md5():
    assert calc_md5(b'mws') == b'mA5nPbh1CSx9M3dbkr3Cyg=='


def test_calc_request_description(access_key, account_id):
    request_description = calc_request_description({
        'AWSAccessKeyId': access_key,
        'Markets': account_id,
        'SignatureVersion': '2',
        'Timestamp': '2017-08-12T19%3A40%3A35Z',
        'Version': '2017-01-01',
        'SignatureMethod': 'HmacSHA256',
    })
    assert not request_description.startswith('&')
    assert request_description == \
        'AWSAccessKeyId=' + access_key + \
        '&Markets=' + account_id + \
        '&SignatureMethod=HmacSHA256' \
        '&SignatureVersion=2' \
        '&Timestamp=2017-08-12T19%3A40%3A35Z' \
        '&Version=2017-01-01'


def test_xml_from_string():
    sample_xml = """
        <note>
            <to>Tove</to>
            <from>Jani</from>
            <heading>Reminder</heading>
            <body>Don't forget me this weekend!</body>
        </note>
    """
    object_dict = xml2dict().fromstring(sample_xml)

    assert object_dict == {
        'note': {
            'to': {'value': 'Tove'},
            'from': {'value': 'Jani'},
            'heading': {'value': 'Reminder'},
            'body': {'value': "Don't forget me this weekend!"}
        }
    }
