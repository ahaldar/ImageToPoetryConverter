import requests
import dataset()

api_file = open("api_details.txt", "r")

api_key = api_file.readline().strip()
api_secret = api_file.readline().strip()
api_file.close()
image_url = 'http://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg'

response = requests.get('https://api.imagga.com/v1/tagging?url=%s' % image_url, auth=(api_key, api_secret))

text =	response.json()

for tag in text['results'][0]['tags']:
	if tag['confidence'] > 70:
		print tag['tag'] , ' ', tag['confidence']

for tag in text['results'][0]['tags']:
    if tag['confidence'] > 70:
        table.insert(url=image_url, tag=tag['tag'], confidence=tag['confidence'])