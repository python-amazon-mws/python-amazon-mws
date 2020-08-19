# -*- coding: utf-8 -*-
"""Amazon OffAmazonPayments Sandbox API."""

from mws import MWS


# TODO fill in docstring links to each of these operations.
# TODO clean up docstrings to a standard format.


class OffAmazonPayments(MWS):
    """Amazon OffAmazonPayments Sandbox API.

    Docs:
    https://pay.amazon.com/us/developer/documentation/apireference/201751630
    """

    SANDBOX_URI = "/OffAmazonPayments_Sandbox/2013-01-01/"
    URI = "/OffAmazonPayments/2013-01-01/"
    VERSION = "2013-01-01"

    def authorize(self, order_ref, order_total, auth_id, timeout=60):
        return self.make_request(
            "Authorize",
            {
                "AmazonOrderReferenceId": order_ref,
                "AuthorizationReferenceId": auth_id,
                "TransactionTimeout": timeout,
                "AuthorizationAmount.Amount": "{:.2f}".format(order_total),
                "AuthorizationAmount.CurrencyCode": "USD",
            },
        )

    def get_authorization_status(self, auth_id):
        return self.make_request(
            "GetAuthorizationDetails", {"AmazonAuthorizationId": auth_id}
        )

    def capture(self, auth_id, amount, capture_id, notes="", currency="USD"):
        """Captures funds
        :param auth_id: the authorization id you want to capture
        :param amount: the amount you wish to capture
        :param capture_id: An id that you make up
        :return: direct response from amazon
        """
        return self.make_request(
            "Capture",
            {
                "AmazonAuthorizationId": auth_id,
                "CaptureReferenceId": capture_id,
                "SellerCaptureNote": notes,
                "CaptureAmount.Amount": "{:.2f}".format(amount),
                "CaptureAmount.CurrencyCode": currency,
            },
        )

    def get_capture_details(self, capture_id):
        return self.make_request("GetCaptureDetails", {"AmazonCaptureId": capture_id})

    def close_authorization(self, auth_id):
        """Call to close an authorization after the total amount of
        the authorization has been captured.
        """
        return self.make_request(
            "CloseAuthorization", {"AmazonAuthorizationId": auth_id}
        )

    def refund(self, capture_id, amount, refund_id, notes="", currency="USD"):
        """Refunds a captured payment
        :param capture_id: the id of the captured payment
        :param amount: the amount to refund
        :param refund_id: a made up refund id for your reference
        :param notes:
        :param currency:
        :return: the direct return value from amazon
        """
        return self.make_request(
            "Refund",
            {
                "AmazonCaptureId": capture_id,
                "RefundReferenceId": refund_id,
                "SellerRefundNote": notes,
                "RefundAmount.Amount": "{:.2f}".format(amount),
                "RefundAmount.CurrencyCode": currency,
            },
        )

    def get_refund_details(self, refund_id):
        """Call to query the status of a particular refund.
        If you received a Pending status when you called the Refund operation,
        you can call this operation to get the current status.
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
