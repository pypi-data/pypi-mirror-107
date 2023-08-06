# netlify-py

A python client for creating, managing and deploying sites to Netlify using the [Netlify API](https://open-api.netlify.com/).

For more info refer their official documentation at [Netlify docs](https://docs.netlify.com/api/get-started/).




## Quick start

1. Install netlify-py

    ```
    pip install netlify-py
    ```

2. Create an instance by passing a [personal access token](https://app.netlify.com/user/applications#personal-access-tokens)
   ```
   from netlify_py import NetlifyPy
   n = NetlifyPy(access_token="zYR6c7fjFYdmxvMW03Vs1qYOIIImXT3sLGPf50hW2AE")
   ```

3. Example usage
   ```
   # return all sites
   sites = n.sites.list_sites()
   
   # get a specific site
   site = n.sites.get_site("site_id")
   
   # create a new site
   new_site = n.sites.create_site()
   
   # list all deploys for a site
   deploys = n.deploys.list_site_deploys("site_id")
   
   # create a deploy of all files in a dir
   new_deploy = n.deploys.deploy_site("site_id","dir_to_deploy")
   
   # get a deploy
   deploy = n.deploys.get_deploy("deploy_id")
   ```