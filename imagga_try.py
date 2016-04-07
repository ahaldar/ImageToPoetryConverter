import requests
import dataset

api_file = open("api_details.txt", "r")

api_key = api_file.readline().strip()
api_secret = api_file.readline().strip()
api_file.close()
#image_url = 'http://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg'


def get_tags(image_url):
	response = requests.get('https://api.imagga.com/v1/tagging?url=%s' % image_url, auth=(api_key, api_secret))

	text =	response.json()
	tag_list = []
	for tag in text['results'][0]['tags']:
		if tag['confidence'] > 70:
			tag_list += (tag['tag'], tag['confidence'])
			table.insert(url=image_url, tag=tag['tag'], confidence=tag['confidence'])
	return tag_list

def main():
	print "here"
	image_url = raw_input("Please enter the link you want to get a poem from:").strip()
	print get_tags(image_url)


if __name__ == "__main__":
	main()