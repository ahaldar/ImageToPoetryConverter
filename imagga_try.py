import requests

api_key = ''
api_secret = ''
image_url = 'http://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg'

response = requests.get('https://api.imagga.com/v1/tagging?url=%s' % image_url,
                auth=(api_key, api_secret))

print response.json()