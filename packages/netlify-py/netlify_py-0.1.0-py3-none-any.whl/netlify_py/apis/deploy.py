"""Deploy module"""
import hashlib
import mmap
import os

import requests

from netlify_py.apis.api_base import ApiBase


class Deploys(ApiBase):
    """
    Deploy class
    Args:
        access_token (str): netlify access token
        base_url (str): netlify api base url
    """

    def __init__(self, access_token, base_url):
        self._access_token = access_token
        self._base_url = base_url
        super().__init__(access_token)

    # endpoints
    _site_deploys = "sites/{site_id}/deploys"
    _site_deploy = "sites/{site_id}/deploys/{deploy_id}"
    _deploy_file_upload = "deploys/{deploy_id}/files/{file_name}"
    _cancel_site_deploy = "deploys/{deploy_id}/cancel"
    _restore_site_deploy = "sites/{site_id}/deploys/{deploy_id}/restore"
    _rollback_site_deploy = "sites/{site_id}/rollback"
    _deploy = "deploys/{deploy_id}"
    _lock_deploy = "deploys/{deploy_id}/lock"
    _unlock_deploy = "deploys/{deploy_id}/unlock"

    # methods
    def list_site_deploys(self, site_id):
        """
        Lists all deploys for a given site
        Args:
            site_id (string): unique site id

        Returns:
            response (list): contains list of all deploys for given site
        """
        return self._get_request(self._base_url + self._site_deploys.format(site_id=site_id))

    def get_site_deploy(self, deploy_id):
        """
        Get details about a deploy
        Args:
            deploy_id (str): unique deploy id of a site

        Returns:
            response (dict): contains deploy details
        """
        return self._get_request(self._base_url + self._site_deploy.format(deploy_id=deploy_id))

    def deploy_file_upload(self, files, deploy_id, file_name):
        """
        Upload file for a deploy
        Args:
            files (buffer): file buffer
            deploy_id (str): unique deploy id
            file_name (): name of file to upload

        Returns:
            HTTP status code of upload API response
        """
        api_headers = {"content-type": "application/octet-stream",
                       'Authorization': 'Bearer {0}'.format(self._access_token)}
        response = requests.put(
            url=self._base_url + self._deploy_file_upload.format(deploy_id=deploy_id,
                                                                 file_name=file_name),
            headers=api_headers,
            data=files
        )
        return response.status_code

    def deploy_site(self, site_id, deploy_dir):
        """
        Deploy a site and upload files in directory
        Args:
            site_id (str): unique site id
            deploy_dir (str): path to deploy directory

        Returns:
            deploy api response if successful
        """
        files_data = self.create_deploy_data(deploy_dir)
        deploy = \
            self._post_request(data=files_data, url=self._base_url + self._site_deploys.format(site_id=site_id))
        print(deploy)
        for root, _, files in os.walk(deploy_dir):
            for file_name in files:
                with open(os.path.join(root, file_name), 'rb') as current_file_handle:
                    self.deploy_file_upload(files=current_file_handle, deploy_id=deploy['id'], file_name=file_name)
        return deploy

    def cancel_site_deploy(self, deploy_id):
        """
        Cancel a site deploy
        Args:
            deploy_id (str): unique deploy id

        Returns:
            api response body
        """
        return self._get_request(self._base_url + self._cancel_site_deploy.format(deploy_id=deploy_id))

    def restore_site_deploy(self, deploy_id):
        """
        Restore a site deploy
        Args:
            deploy_id (str): unique deploy id

        Returns:
            api response body
        """
        return self._get_request(self._base_url + self._restore_site_deploy.format(deploy_id=deploy_id))

    def rollback_site_deploy(self, deploy_id):
        """
        Rollback a deployed site
        Args:
            deploy_id (str): unique deploy id

        Returns:
            api response body
        """
        return self._get_request(self._base_url + self._rollback_site_deploy.format(deploy_id=deploy_id))

    def get_deploy(self, deploy_id):
        """
        Get a specific deploy details by id
        Args:
            deploy_id (str): unique deploy id

        Returns:
            api response body
        """
        return self._get_request(self._base_url + self._deploy.format(deploy_id=deploy_id))

    @staticmethod
    def create_deploy_data(deploy_dir):
        """
        Creates a list of filenames and their sha1sum
        Args:
            deploy_dir (str): path to folder containing deployment files

        Returns:
            Request JSON body for creating a deploy
        """
        upload_files = {}
        for root, _, files in os.walk(deploy_dir):
            for file_name in files:
                rel_dir = os.path.relpath(root, deploy_dir)
                rel_file = os.path.join(rel_dir, file_name)
                full_path = os.path.join(root, file_name)
                sha1 = hashlib.sha1()
                with open(full_path, 'rb') as file:
                    with mmap.mmap(file.fileno(), 0, prot=mmap.PROT_READ) as memory_map:
                        sha1.update(memory_map)
                upload_files[rel_file.lstrip('./')] = sha1.hexdigest()
        return {"files": upload_files}
