import json
import requests
import sys
import time

def ask_question(attribute, question, sender_id, user_dict):
    if user_dict.get(attribute) is None:
        sendTextMessage(sender_id, question)
    while user_dict.get(attribute) is None:
        wait_for_response()
    sys.stderr.write(str(user_dict)+ '\n')

def wait_for_response():
    returnval = add_listener()
    sys.stderr.write(str(returnval) + '\n')
    time.sleep(1)

def add_listener():
    base_url = "https://graph.facebook.com/v2.6/me/subscribed_apps?access_token="
    token = "CAAYM4P71Md8BAMRPqQyRa7pHVvQyXydWi2LRzZBVoZBPr8qxhLi9ZC1kD26PgFx3IB1E17tTjECLFGn4uerwISpVzuLMmqIaGSgvyMNgF0ix1RZA4x1VGPiKMXCRzJ1B7xH2D2G0fuHGeAroC4gVX8qqxz2aaTbusYz5P82arcy4oV6ZAScwKcZBWfcMauYpUZD"
    url = base_url + token
    r = requests.post(url, headers={"Content-type": "application/json"})
    return r.status_code

def sendTextMessage(sender_id, text):
    token = "CAAYM4P71Md8BAMRPqQyRa7pHVvQyXydWi2LRzZBVoZBPr8qxhLi9ZC1kD26PgFx3IB1E17tTjECLFGn4uerwISpVzuLMmqIaGSgvyMNgF0ix1RZA4x1VGPiKMXCRzJ1B7xH2D2G0fuHGeAroC4gVX8qqxz2aaTbusYz5P82arcy4oV6ZAScwKcZBWfcMauYpUZD"
    url = "https://graph.facebook.com/v2.6/me/messages?access_token="+token
    headers = {'Content-Type': 'application/json'}
    payload = dict(recipient=dict(id=sender_id), message=dict(text=text))
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    sys.stderr.write(str(r.status_code) + '\n')
