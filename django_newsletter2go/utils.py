import requests
from requests.auth import HTTPBasicAuth

from . import API_BASE


class Newsletter(object):
    def __init__(self, **kwargs):
        try:
            items = kwargs.items()
        except AttributeError:
            items = kwargs.iteritems()
        for key, value in items:
            setattr(self, key, value)

    def to_json(self):
        return {
            'name': getattr(self, 'name', ''),
            'html': getattr(self, 'html', ''),
            'subject': getattr(self, 'subject', ''),
            'preheader': getattr(self, 'preheader', ''),
            'header_from_email': getattr(self, 'header_from_email', ''),
            'header_from_name': getattr(self, 'header_from_name', ''),
        }

def get_n2g_token(auth_key, username, password):
    api_call = '/oauth/v2/token'
    params = {
        'username': username,
        'grant_type': 'https://nl2go.com/jwt',
        'password': password,
    }
    response = requests.post(
        API_BASE + api_call,
        json=params,
        auth=HTTPBasicAuth(*auth_key.split(':'))
    )

    return response.json().get('access_token')

def create_mailing(access_token, lid, newsletter):
    api_call = '/lists/{lid}/newsletters'.format(lid=lid)
    params = {
        'lid': lid,
        'newsletter': newsletter.to_json(),
    }
    response = requests.post(
        API_BASE + api_call,
        json=params,
        headers={'Authorization': 'Bearer {access_token}'.format(
            access_token=access_token)}
    )

    return response.json().get('value', {}).get('id')
