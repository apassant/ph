import requests

OLDEST_DAY = '2013-11-24'

API_ROOT = 'https://api.producthunt.com'

class ProductHunt(object):

    def __init__(self, api_key, api_secret):
        """Set-up the API.

        Stores the API key and secret in the object, and request
        a new API token to be used in subsequent calls."""
        self.api_key = api_key
        self.api_secret = api_secret
        self._get_token()

    def _get(self, path, params=None):
        return self._query(path, params, method='GET')
    def _post(self, path, params=None):
        return self._query(path, params, method='POST')

    def _query(self, path, params=None, method='GET'):
        if not params:
            params = {}
        headers = {} 
        if hasattr(self, 'access_token'):
            headers.update({
                'Authorization' : 'Bearer %s' %(self.access_token)
            })
        if method == 'GET':
            r = requests.get('%s%s' %(API_ROOT, path), params=params, headers=headers)
        else:
            r = requests.post('%s%s' %(API_ROOT, path), params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
        return {}
  
    def _get_token(self):
        """Get an API token."""
        data = self._post('/v1/oauth/token', params={
             "client_id": self.api_key,
             "client_secret": self.api_secret,
             "grant_type": "client_credentials"
        })
        self.access_token = data.get('access_token') 

 #   def get_posts(self, **kwargs=None):
  ###      """Get a list of posts."""

    def get_post(self, post_id):
        """Get details about a product."""
        return self._get('/v1/posts/{post_id}'.format(**{
            'post_id' : post_id
        }))

if __name__ == '__main__':
    ph = ProductHunt(API_KEY, API_SECRET)
    print ph.get_post(3)

