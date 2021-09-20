# -*- coding: utf-8 -*-
"""Amazon OffAmazonPayments Sandbox API."""

from mws import MWS


class OffAmazonPayments(MWS):
    """Amazon OffAmazonPayments Sandbox API.

    Docs: https://amazonpaylegacyintegrationguide.s3.amazonaws.com/docs/amazon-pay-api/intro.html
    """

    SANDBOX_URI = "/OffAmazonPayments_Sandbox/2013-01-01/"
    URI = "/OffAmazonPayments/2013-01-01/"
    VERSION = "2013-01-01"

    def authorize(self, order_ref, order_total, auth_id, timeout=60, currency="USD"):
        """Reserves a specified amount against the payment methods stored in
        the order reference.

        Docs: https://amazonpaylegacyintegrationguide.s3.amazonaws.com/docs/amazon-pay-api/authorize.html

        :param order_ref: reference identifier for the order
        :param order_total: amount to be authorized
        :param auth_id: client-side reference, should be unique, shorter than 32
                        chars, and only composed of ASCII letters, numbers,
                        ``-``, and ``_``
        :param timeout: duration of the authorization, in minutes, after the
                        delay has expired the authorization is automatically
                        rescinded

                        can be any multiple of 5 between 5 and 1440 (24 hours)
        :param currency: ISO 4217 currency code for the amount to authorize
        :returns: authorization details (https://amazonpaylegacyintegrationguide.s3.amazonaws.com/docs/amazon-pay-api/authorizationdetails.html)
        """
        return self.make_request(
            "Authorize",
            {
                "AmazonOrderReferenceId": order_ref,
                "AuthorizationReferenceId": auth_id,
                "TransactionTimeout": timeout,
                "AuthorizationAmount.Amount": f"{order_total:.2f}",
                "AuthorizationAmount.CurrencyCode": currency,
            },
        )

    def get_authorization_status(self, auth_id):
        """Retrieves the details of an authorization.

        Docs: https://amazonpaylegacyintegrationguide.s3.amazonaws.com/docs/amazon-pay-api/getauthorizationdetails.html

        :param auth_id: the authorization id to query, should be the
                        ``AmazonAuthorizationId`` from the authorization details
        :returns: authorization details (as with :meth:`~.authorize`)
        """
        return self.make_request(
            "GetAuthorizationDetails", {"AmazonAuthorizationId": auth_id}
        )

    def capture(self, auth_id, amount, capture_id, notes="", currency="USD"):
        """Captures funds

        Docs: https://amazonpaylegacyintegrationguide.s3.amazonaws.com/docs/amazon-pay-api/capture.html

        :param auth_id: the authorization id you want to capture
        :param amount: the amount you wish to capture
        :param capture_id: An id that you make up
        :param notes: description shown to the buyer in emails, 255 characters
                      max
        :param currency: ISO 4217 currency code (e.g. USD, EUR, ...) for the
                         amount to capture
        :return: capture details (https://amazonpaylegacyintegrationguide.s3.amazonaws.com/docs/amazon-pay-api/getcapturedetails.html)
        """
        return self.make_request(
            "Capture",
            {
                "AmazonAuthorizationId": auth_id,
                "CaptureReferenceId": capture_id,
                "SellerCaptureNote": notes,
                "CaptureAmount.Amount": f"{amount:.2f}",
                "CaptureAmount.CurrencyCode": currency,
            },
        )

    def get_capture_details(self, capture_id):
        """Retrieves the details of a capture

        Docs: https://amazonpaylegacyintegrationguide.s3.amazonaws.com/docs/amazon-pay-api/getcapturedetails.html

        :param capture_id: the identifier for the capture
        :returns: capture details (see :meth:`~.capture`)
        """
        return self.make_request("GetCaptureDetails", {"AmazonCaptureId": capture_id})

    def close_authorization(self, auth_id, reason=None):
        """Close an authorization without capturing it.

        Docs: https://amazonpaylegacyintegrationguide.s3.amazonaws.com/docs/amazon-pay-api/closeauthorization.html

        :param auth_id: the id of the authorization to close
        :param reason: reason for closing the authorization, will be shown to
                       customers, up to 255 characters
        """
        params = {"AmazonAuthorizationId": auth_id}
        if reason:
            params["ClosureReason"] = reason
        return self.make_request("CloseAuthorization", params)

    def refund(self, capture_id, amount, refund_id, notes="", currency="USD"):
        """Refunds a captured payment

        Docs: https://amazonpaylegacyintegrationguide.s3.amazonaws.com/docs/amazon-pay-api/refund.html

        :param capture_id: the id of the captured payment
        :param amount: the amount to refund
        :param refund_id: a made up refund id for your reference
        :param notes: description of the refund shown to the customer, up to
                      255 characters
        :param currency: ISO 4217 currency code for the ``amount``
        :return: refund details (https://amazonpaylegacyintegrationguide.s3.amazonaws.com/docs/amazon-pay-api/refunddetails.html)
        """
        return self.make_request(
            "Refund",
            {
                "AmazonCaptureId": capture_id,
                "RefundReferenceId": refund_id,
                "SellerRefundNote": notes,
                "RefundAmount.Amount": f"{amount:.2f}",
                "RefundAmount.CurrencyCode": currency,
            },
        )

    def get_refund_details(self, refund_id):
        """Call to query the status of a particular refund.

        If you received a Pending status when you called the Refund operation,
        you can call this operation to get the current status.

        :param refund_id: the refund's identifier
        :return: the refund details (see :meth:`~.refund`)
        """
        return self.make_request("GetRefundDetails", {"AmazonRefundId": refund_id})

    def get_billing_agreement_details(self, order_ref, address_consent_token):
        return self.make_request(
            "GetBillingAgreementDetails",
            {
                "AmazonBillingAgreementId": order_ref,
                "AddressConsentToken": address_consent_token,
            },
        )

    def get_order_reference_details(self, order_ref, address_consent_token=""):
        data = {"AmazonOrderReferenceId": order_ref}
        if address_consent_token:
            data["AddressConsentToken"] = address_consent_token
        return self.make_request("GetOrderReferenceDetails", data)

    def set_order_reference_details(
        self,
        order_ref,
        order_total,
        store_name,
        order_id=None,
        note=None,
        currency="USD",
    ):
        data = {
            "AmazonOrderReferenceId": order_ref,
            "OrderReferenceAttributes.OrderTotal.Amount": order_total,
            "OrderReferenceAttributes.OrderTotal.CurrencyCode": currency,
            "OrderReferenceAttributes.SellerOrderAttributes.SellerOrderId": order_id,
            "OrderReferenceAttributes.SellerOrderAttributes.StoreName": store_name,
            "OrderReferenceAttributes.SellerNote": note,
        }
        return self.make_request("SetOrderReferenceDetails", data)

    def confirm_order_reference(self, order_ref):
        return self.make_request(
            "ConfirmOrderReference", {"AmazonOrderReferenceId": order_ref}
        )

    def cancel_order_reference(self, order_ref):
        return self.make_request(
            "CancelOrderReference", {"AmazonOrderReferenceId": order_ref}
        )

    def close_order_reference(self, order_ref):
        return self.make_request(
            "CloseOrderReference", {"AmazonOrderReferenceId": order_ref}
        )
