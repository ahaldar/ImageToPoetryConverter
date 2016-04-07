import requests

api_key = 'acc_46e44eb085cf6f7'
api_secret = '924599341f274a449f772aa4ef820351'
image_url = 'http://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg'

response = requests.get('https://api.imagga.com/v1/tagging?url=%s' % image_url,
                auth=(api_key, api_secret))

print response.json()