#!/usr/bin/env python
import requests
import dataset
import json
import flask

from flask import Flask
from flask import jsonify
from flask import render_template

from flask.ext.cors import CORS

backend = Flask(__name__)
CORS(backend)
# frontend = Flask(__name__, template_folder='Frontend')

'''
Running the program:
Run python backend.py
Open up the browser and go to 127.0.0.1/url/<path>
Blah blah
Example URL http://127.0.0.1:5000/url/http://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg
'''
@backend.route("/")
def index():
    return render_template('index.html')

@backend.route("/index2")
def index2():
    return render_template('index2.html')

@backend.route('/url/<path:path>')
def url(path):
    image_url = path
    tags = get_tags(image_url)
    print "tags are"
    for tag in tags:
        print tag[0]
    poem = json.loads(get_poem(tags))
    return flask.jsonify(**poem)


@backend.route('/rating/<rating_val>/<poem>/<path:path>')
def rating(rating_val, poem, path):
    print 'rating is ' + ' ' + str(rating_val)
    print 'poem is ' + poem
    print 'path is ' + path
    get_rating_from_front_end(path, poem, rating_val)
    return "rating_recd"

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

    text =  response.json()
    tag_list = []
    try:
        for tag in text['results'][0]['tags']:
            if tag['confidence'] > 15:
                tag_list.append((tag['tag'], tag['confidence']))
                image_tag_table.insert(dict(url=image_url, tag=tag['tag'], confidence=tag['confidence']))

        if not tag_list:
            tag = text['results'][0]['tags'][0]
            tag_list.append((tag['tag'], tag['confidence']))
            image_tag_table.insert(dict(url=image_url, tag=tag['tag'], confidence=tag['confidence']))
        
        print_database(image_url)
    except:
        tag_list = [('animal', 0.343)]
    return tag_list

def print_database(image_url):
    print image_tag_table.find_one(url=image_url)

def print_tag_poem(tag):
    print tag_poem_table.find_one(tag=tag)

'''returns a json containing all details of the poem'''
def get_poem(taglist):
    tagsize = len(taglist)
    count = min(tagsize,3)
    found = False
    for tagJson in taglist[:count]:
        tag = tagJson[0]
        if(tag_poem_table.find_one(tag=tag)):
                print_tag_poem(tag)
                return tag_poem_table.find_one(tag=tag)['poem']
    for tagJson in taglist[:count]:
        tag = tagJson[0]
        try:
            if(tag_poem_table.find_one(tag=tag)):
                print_tag_poem(tag)
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
                    print_tag_poem(tag)
                    return poem_string
            for poem in response_small.json():
                if poem['linecount'] == min_lc:
                    poem_string = json.dumps(poem)
                    tag_poem_table.insert(dict(tag=tag, poem=poem_string))
                    print_tag_poem(tag)
                    return poem_string
        except:
            continue
    if not found:
        poem_string = json.dumps({"title": "Ozymandias",
        "author": "Percy Bysshe Shelley",
        "lines": [
      "I met a traveller from an antique land",
      "Who said: Two vast and trunkless legs of stone",
      "Stand in the desert...Near them, on the sand,",
      "Half sunk, a shattered visage lies, whose frown,",
      "And wrinkled lip, and sneer of cold command,",
      "Tell that its sculptor well those passions read",
      "Which yet survive, stamped on these lifeless things,",
      "The hand that mocked them, and the heart that fed:",
      "And on the pedestal these words appear:",
      "'My name is Ozymandias, king of kings:",
      "Look on my works, ye Mighty, and despair!'",
      "Nothing beside remains. Round the decay",
      "Of that colossal wreck, boundless and bare",
      "The lone and level sands stretch far away."
        ],
        "linecount": "14"
        })
        print("Default poem printed")
        return poem_string


# def get_rating(image_url, poem):
#   rating = raw_input("Please enter a rating from 1 to 10: ").strip()
#   # print("In get_rating")
#   # print(type(poem))
#   result_rating_table.insert(dict(url=image_url, poem=str(poem), rating=rating))
def get_rating_from_front_end(image_url, poem, rating):
    result_rating_table.insert(dict(url=image_url, poem=str(poem), rating=rating))
    

def main():
    print "main"
    # image_url = raw_input("Please enter the link you want to get a poem from:").strip()
    # tags = get_tags(image_url)
    # poem = json.loads(get_poem(tags[0][0]))
    # print_tag_poem(tags[0][0])
    # print poem
    # get_rating(image_url, poem)


if __name__ == '__main__':
    backend.run(debug=True, host='0.0.0.0')
