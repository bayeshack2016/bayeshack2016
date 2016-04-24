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
QUESTIONS = dict(
    city='What city do you live in?',
    job='What do you do for a living?',
    experience='How many years of experience do you have in that job?',
    education='Education? ("Less Than High School", "High School" , "Some College", "College", "Advanced")',
    gender='What gender do you identify as?',
)
USER_PROFILE = {}
CURRENT_ATTRIBUTE='city'
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
    USER_PROFILE[CURRENT_ATTRIBUTE] = text
    sendTextMessage(sender_id, 'Thank you!')

def ask_questions():
    global CURRENT_ATTRIBUTE
    for attribute, question in QUESTIONS.iteritems():
        while USER_PROFILE.get(attribute) is None:
            CURRENT_ATTRIBUTE = attribute
            sendTextMessage(SENDER_ID, question)
            time.sleep(10)
        sys.stderr.write(str(USER_PROFILE) + '\n')


def main():
    app.run(debug=True)
    ask_questions()


if __name__ == "__main__":
    main()
