from collections import namedtuple
from flask import Flask
from flask import request
# from rq import Queue
# from worker import conn
import json
import requests
import sys
import time
import traceback

app = Flask(__name__)
UserProfile = namedtuple('User', 'city job years_exp education gender')
QUESTIONS = [
    'What city do you live in?',
    'What do you do for a living?',
    'How many years of experience do you have in that job?',
    'Education? ("Less Than High School", "High School" , "Some College", "College", "Advanced")',
    'What gender do you identify as?',
]
USER_PROFILE = UserProfile(
    city=None,
    job=None,
    years_exp=None,
    education=None,
    gender=None
)
INDEX_OF_CURRENT_QUESTION=0
SENDER_ID=1020675814687539

@app.route("/")
def ind():
    return "Hello World!"

@app.route('/webhook', methods=['GET', 'POST'])
def validate():
    try:
        # sys.stderr.write(str(q) + '\n')
        # result = q.enqueue(add_listener)
        # sys.stderr.write(str(result) + '\n')
        if request.method == 'GET':
            if request.args.get('hub.verify_token') == 'verify_me':
                return request.args.get('hub.challenge')
        else:
            messaging_events = json.loads(request.data.decode("utf-8"))
            messages = messaging_events['entry'][0]['messaging']
            sys.stderr.write(str(messaging_events) + '\n')
            for event in messages:
                if (event.get('message') and event['message']['text']):
                    sender_id = event['sender']['id']
                    text = event['message']['text']
                    # Handle a text message from this sender
                    # sendTextMessage(sender_id, text)
                    store_response(sender_id, text)
                    return text
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        app.logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))
        return 'Error, wrong validation token'

def sendTextMessage(sender_id, text):
    token = "CAAYM4P71Md8BAMRPqQyRa7pHVvQyXydWi2LRzZBVoZBPr8qxhLi9ZC1kD26PgFx3IB1E17tTjECLFGn4uerwISpVzuLMmqIaGSgvyMNgF0ix1RZA4x1VGPiKMXCRzJ1B7xH2D2G0fuHGeAroC4gVX8qqxz2aaTbusYz5P82arcy4oV6ZAScwKcZBWfcMauYpUZD"
    url = "https://graph.facebook.com/v2.6/me/messages?access_token="+token
    headers = {'Content-Type': 'application/json'}
    payload = dict(recipient=dict(id=sender_id), message=dict(text=text))
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    sys.stderr.write(str(r.status_code) + '\n')

def store_response(sender_id, text):
    global USER_PROFILE
    USER_PROFILE[INDEX_OF_CURRENT_QUESTION] = text
    sendTextMessage(sender_id, 'Thank you!')


def main():
    app.run(debug=True)
    global INDEX_OF_CURRENT_QUESTION
    for i, question in enumerate(QUESTIONS):
        # if user response to that question is not there
        while USER_PROFILE[i] is None:
            INDEX_OF_CURRENT_QUESTION=i
            sendTextMessage(SENDER_ID, question)
            time.sleep(10)
        sys.stderr.write(str(USER_PROFILE) + '\n')


if __name__ == "__main__":
    main()
