"""NetlifyPy module"""
from netlify_py.apis.deploy import Deploys
from netlify_py.apis.sites import Sites


class NetlifyPy:
    """
    The NetlifyPy class providing blackbox use of the Netlify REST API.
    This is the main class of the API module. This should be the only class used in
    applications built around the API.
    Args:
        access_token (str): netlify access token
    """

    def __init__(self, access_token):
        self.__base_url = 'https://api.netlify.com/api/v1/'
        self.__access_token = access_token

        self.sites = Sites(self.__access_token, self.__base_url)
        self.deploys = Deploys(self.__access_token, self.__base_url)
