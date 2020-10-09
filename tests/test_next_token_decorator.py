"""
Testing the `next_token_action` decorator on a toy class.
"""
import mws

# pylint: disable=invalid-name

ACTION = "SomeAction"


class ToyClass(object):
    """
    Example class using a method designed to be run with a `next_token`,
    calling the corresponding `action_by_next_token` method
    """

    def __init__(self):
        self.method_run = None

    def action_by_next_token(self, action, token):
        """
        Toy next-action method, simply returns the action and token together.
        The decorator should call THIS method automatically if a next_token kwarg
        is present in the target call.
        """
        self.method_run = "action_by_next_token"
        # Modify the action similar to how live code does it,
        # for the sake of our sanity here.
        modified_action = "{}ByNextToken".format(action)
        return modified_action, token

    @mws.utils.next_token_action(ACTION)
    def target_request_method(self, next_token=None):
        """
        Toy request method, used as the target for our test.
        """
        self.method_run = "target_function"
        return ACTION, next_token


def test_request_run_normal():
    """
    Call the target request method with no next_token, and we should
    see that method run normally.
    """
    instance = ToyClass()
    action, token = instance.target_request_method()
    assert action == ACTION
    assert token is None
    assert instance.method_run == "target_function"


def test_request_run_with_next_token():
    """
    Call the target request method with no next_token, and we should
    see that method run normally.
    """
    instance = ToyClass()
    next_token = "Olly Olly Oxen Free!"
    action, token = instance.target_request_method(next_token=next_token)
    what_action_should_be = "{}ByNextToken".format(ACTION)
    assert action == what_action_should_be
    assert token == next_token
    assert instance.method_run == "action_by_next_token"
