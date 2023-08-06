"""Sites module"""
from netlify_py.apis.api_base import ApiBase


class Sites(ApiBase):
    """
    Sites API Class
    Args:
        access_token (str): netlify access token
        base_url (str): netlify api base url
    """

    def __init__(self, access_token, base_url):
        self._base_url = base_url
        super().__init__(access_token)

    # endpoints
    _sites = "sites/?per_page=100"
    _site = "sites/{site_id}"
    _account_sites = "{account_slug}/sites/?page_size=100".format(account_slug="{account_slug}")

    # methods
    def list_sites(self):
        """
        List all sites on netlify

        Returns:
            list of sites
        """
        return self._get_request(self._base_url + self._sites)

    def get_site(self, site_id):
        """
        Get a specific site details
        Args:
            site_id (str): unique site id

        Returns:
            site details
        """
        return self._get_request(self._base_url + self._site.format(site_id=site_id))

    def create_site(self, name=None):
        """
        Create a new site on netlify
        Args:
            name (str): a unique name for site (optional)
        Returns:
            newly created site details
        """
        return self._post_request(data={"name": name}, url=self._base_url + self._sites)
