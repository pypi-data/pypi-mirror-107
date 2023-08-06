"""APIBase module"""
import json

import requests

from netlify_py.apis.exceptions import WrongParamsError, InvalidTokenError, SemanticError, InternalServerError, \
    NetlifyPyError, NotFoundError


class ApiBase:
    """
    Base class for handling API requests
    Parameters:
        access_token (str): netlify access token
    """

    def __init__(self, access_token):
        self.__access_token = access_token

    def _get_request(self, url, params=None):
        """
        Creates a HTTP GET request
        Args:
            url (str): api url
            params (list): list of query param dicts

        Returns:
            response from API (dict)
        """
        api_headers = {'Authorization': 'Bearer {0}'.format(self.__access_token)}
        api_params = {}

        if params is not None:
            for k in params:
                # ignore all unused params
                if not params[k] is None:
                    param = params[k]

                    # convert boolean to lowercase string
                    if isinstance(param, bool):
                        param = str(param).lower()

                    api_params[k] = param

        response = requests.get(
            url,
            headers=api_headers,
            params=api_params
        )

        if response.status_code == 200:
            result = json.loads(response.text)
            return result

        if response.status_code == 401:
            raise InvalidTokenError('Invalid token, try to refresh it', response.text)

        if response.status_code == 404:
            raise NotFoundError('Requested resource not found', response.text)

        raise NetlifyPyError('Error: {0}'.format(response.status_code), response.text)

    def _post_request(self, data, url, api_headers=None):
        """
        Makes a HTTP POST request
        Parameters:
            data (dict): POST body data
            url (str): API url
            api_headers (dict): API headers
        Returns:
            response from API (dict)
        """
        if api_headers is None:
            api_headers = {}
        api_headers['Authorization'] = 'Bearer {0}'.format(self.__access_token)
        response = requests.post(
            url,
            headers=api_headers,
            json=data
        )
        if response.status_code == 200:
            result = json.loads(response.text)
            return result

        if response.status_code == 201:
            result = json.loads(response.text)
            return result

        if response.status_code == 400:
            raise WrongParamsError('Some of the parameters are wrong', response.text)

        if response.status_code == 404:
            raise NotFoundError('Requested resource not found', response.text)

        if response.status_code == 401:
            raise InvalidTokenError('Invalid access token, replace it', response.text)

        if response.status_code == 422:
            raise SemanticError('Error: {0}'.format(response.status_code), response.text)

        if response.status_code == 500:
            raise InternalServerError('Internal server error', response.text)

        raise NetlifyPyError('Error: {0}'.format(response.status_code), response.text)
