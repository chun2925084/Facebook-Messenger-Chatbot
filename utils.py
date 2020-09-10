#import os
#coding:utf-8
import requests
import json
import os
# from verify import access_token

GRAPH_URL = "https://graph.facebook.com/v2.6"
# ACCESS_TOKEN = access_token

## for heroku
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


def send_button_message(id, button, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment":{
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons":button
                }
            }
        }
    }

    response = requests.post(url, json = payload)
    if response.status_code!=200:
        print(response)
        print("Unable to send" +response.text)
    return response


def send_image_url(id, img_url):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment":{
                "type": "image",
                "payload": {
                    "url": img_url,
                    "is_reusable":True
                }
            }
        }
    }

    response = requests.post(url, json = payload)
    if response.status_code!=200:
        print(response)
        print("Unable to send" +response.text)
    return response
 
