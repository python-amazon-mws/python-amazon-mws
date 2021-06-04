from mws.mws import calc_md5, calc_request_description, clean_params_dict


def test_calc_md5():
    assert calc_md5(b"mws") == b"mA5nPbh1CSx9M3dbkr3Cyg=="


def test_calc_request_description(access_key, account_id):
    request_description = calc_request_description(
        {
            "AWSAccessKeyId": access_key,
            "Markets": account_id,
            "SignatureVersion": "2",
            "Timestamp": "2017-08-12T19%3A40%3A35Z",
            "Version": "2017-01-01",
            "SignatureMethod": "HmacSHA256",
        }
    )
    assert not request_description.startswith("&")
    assert (
        request_description
        == "AWSAccessKeyId="
        + access_key
        + "&Markets="
        + account_id
        + "&SignatureMethod=HmacSHA256"
        "&SignatureVersion=2"
        "&Timestamp=2017-08-12T19%3A40%3A35Z"
        "&Version=2017-01-01"
    )


def test_calc_request_description_for_cleaned_params(access_key, account_id):
    params = clean_params_dict(
        {
            "AWSAccessKeyId": access_key,
            "Markets": account_id,
            "Subscription.Destination.AttributeList.member.1.Key": "sqsQueueUrl",
            "Subscription.Destination.AttributeList.member.1.Value": "https://sqs.us-east-1.amazonaws.com/123456789/mws-notifications",
            "SignatureVersion": "2",
            "Timestamp": "2017-08-12T19:40:35Z",
            "Version": "2017-01-01",
            "SignatureMethod": "HmacSHA256",
        }
    )
    request_description = calc_request_description(params)

    assert not request_description.startswith("&")
    assert request_description == (
        "AWSAccessKeyId="
        + access_key
        + "&Markets="
        + account_id
        + "&SignatureMethod=HmacSHA256"
        "&SignatureVersion=2"
        "&Subscription.Destination.AttributeList.member.1.Key=sqsQueueUrl"
        "&Subscription.Destination.AttributeList.member.1.Value="
        "https%3A%2F%2Fsqs.us-east-1.amazonaws.com%2F123456789%2Fmws-notifications"
        "&Timestamp=2017-08-12T19%3A40%3A35Z"
        "&Version=2017-01-01"
    )
