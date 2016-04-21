#!/usr/bin/env python
import requests
import dataset
import json

api_file = open("api_details.txt", "r")

api_key = api_file.readline().strip()
api_secret = api_file.readline().strip()
api_file.close()
db = dataset.connect('sqlite:///testing.db')
image_tag_table = db['links_table']
tag_poem_table = db['poem_table']
result_rating_table = db['rating_table']
#image_url = 'http://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg'


def get_tags(image_url):
	response = requests.get('https://api.imagga.com/v1/tagging?url=%s' % image_url, auth=(api_key, api_secret))

	text =	response.json()
	tag_list = []
	for tag in text['results'][0]['tags']:
		if tag['confidence'] > 15:
			tag_list.append((tag['tag'], tag['confidence']))
			image_tag_table.insert(dict(url=image_url, tag=tag['tag'], confidence=tag['confidence']))

	if not tag_list:
		tag = text['results'][0]['tags'][0]
		tag_list.append((tag['tag'], tag['confidence']))
		image_tag_table.insert(dict(url=image_url, tag=tag['tag'], confidence=tag['confidence']))
	
	print_database(image_url)
	return tag_list

def print_database(image_url):
	print image_tag_table.find_one(url=image_url)

def print_tag_poem(tag):
	print tag_poem_table.find_one(tag=tag)

'''returns a json containing all details of the poem'''
def get_poem(tag):
	if(tag_poem_table.find_one(tag=tag)):
		return tag_poem_table.find_one(tag=tag)['poem']
	response_cap = requests.get('http://poetrydb.org/lines/' + tag.title()) 
	response_small = requests.get('http://poetrydb.org/lines/' + tag.lower())
	min_lc_cap = min([poem['linecount'] for poem in response_cap.json()])
	min_lc_small = min([poem['linecount'] for poem in response_small.json()])
	min_lc = min(min_lc_small, min_lc_small)
	poem_string = ''
	for poem in response_cap.json():
		if poem['linecount'] == min_lc:
			poem_string = json.dumps(poem)
			tag_poem_table.insert(dict(tag=tag, poem=poem_string))
			return poem_string
	for poem in response_small.json():
		if poem['linecount'] == min_lc:
			poem_string = json.dumps(poem)
			tag_poem_table.insert(dict(tag=tag, poem=poem_string))
			return poem_string

def get_rating(image_url, poem):
	rating = raw_input("Please enter a rating from 1 to 10: ").strip()
	# print("In get_rating")
	# print(type(poem))
	result_rating_table.insert(dict(url=image_url, poem=str(poem), rating=rating))


def main():
	print "here"
	image_url = raw_input("Please enter the link you want to get a poem from:").strip()
	tags = get_tags(image_url)
	poem = json.loads(get_poem(tags[0][0]))
	print_tag_poem(tags[0][0])
	print poem
	get_rating(image_url, poem)
if __name__ == "__main__":
	main()