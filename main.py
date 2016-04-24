from flask import Flask
from flask import request
from rq import Queue
from worker import conn
import json
import sys
import traceback
from utils import ask_question
from utils import wait_for_response

app = Flask(__name__)
q = Queue(connection=conn)

QUESTIONS = dict(
    city='What city do you live in?',
    job='What do you do for a living?',
    experience='How many years of experience do you have in that job?',
    education='Education? ("Less Than High School", "High School" , "Some College", "College", "Advanced")',
    gender='What gender do you identify as?',
)
CURRENT_ATTRIBUTE=None
USER_PROFILE = {}
SENDER_ID=1020675814687539

@app.route("/")
def ind():
    return "Hello World!"

@app.route('/webhook', methods=['GET', 'POST'])
def validate():
    try:
        ask_questions()
        if request.method == 'GET':
            if request.args.get('hub.verify_token') == 'verify_me':
                return request.args.get('hub.challenge')
        else:
            messaging_events = json.loads(request.data.decode("utf-8"))
            messages = messaging_events['entry'][0]['messaging']
            sys.stderr.write(str(messaging_events) + '\n')
            for event in messages:
                if (event.get('message') and event['message']['text']):
                    text = event['message']['text']
                    # Handle a text message from this sender
                    store_attribute(USER_PROFILE, text)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        app.logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))
        return 'Error, wrong validation token'

def store_attribute(user_profile, text):
    for attribute in QUESTIONS:
        if user_profile.get(attribute) is None:
            user_profile[attribute] = text
            sys.stderr.write(str(user_profile) + '\n')

def ask_questions():
    for attribute, question in QUESTIONS.iteritems():
        if USER_PROFILE.get(attribute) is None:
            q.enqueue(
                ask_question,
                (
                    attribute,
                    question,
                    SENDER_ID,
                    USER_PROFILE
                )
            )


def main():
    wait_for_response()
    app.run(debug=True)


if __name__ == "__main__":
    main()
