"""NetlifyPyError module"""


class NetlifyPyError(Exception):
    """
    The base exception class for NetlifyPy.
    Parameters:
        msg (str): Short description of the error.
        response: Error response from the API call.
    """

    def __init__(self, msg, response=None):
        super().__init__(msg)
        self.message = msg
        self.response = response

    def __str__(self):
        return repr(self.message + " " + self.response)


class UnauthorizedClientError(NetlifyPyError):
    """Wrong access token, 401 error."""


class BadRequestError(NetlifyPyError):
    """Request body or params are wrong, 400 error."""


class InternalServerError(NetlifyPyError):
    """Internal server errors, 500 error."""


class InvalidTokenError(NetlifyPyError):
    """Wrong/non-existing access token, 401 error."""


class WrongParamsError(NetlifyPyError):
    """Some of the parameters (HTTP params or request body) are wrong, 400 error."""


class SemanticError(NetlifyPyError):
    """Well formed request but was unable to process due to semantic errors"""


class NotFoundError(NetlifyPyError):
    """object or resource not found on server"""
