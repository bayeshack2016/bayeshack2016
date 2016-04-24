# import os
import time
import sys
from utils import add_listener
from utils import sendTextMessage

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

# import redis
# from rq import Worker, Queue, Connection

# listen = ['high', 'default', 'low']

# redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

# conn = redis.from_url(redis_url)

# if __name__ == '__main__':
#     with Connection(conn):
#         worker = Worker(map(Queue, listen))
#         worker.work()
def ask_questions():
    global CURRENT_ATTRIBUTE
    for attribute, question in QUESTIONS.iteritems():
        while USER_PROFILE.get(attribute) is None:
            CURRENT_ATTRIBUTE = attribute
            sendTextMessage(SENDER_ID, question)
            wait_for_response()
        sys.stderr.write(str(USER_PROFILE) + '\n')

def store_response(sender_id, text):
    global USER_PROFILE
    USER_PROFILE[CURRENT_ATTRIBUTE] = text
    sendTextMessage(sender_id, 'Thank you!')

def wiat_for_response():
    returnval = add_listener()
    sys.stderr.write(str(returnval) + '\n')
    time.sleep(5)

def main():
    if CURRENT_ATTRIBUTE is None:
        ask_questions()

if __name__ == '__main__':
    main()
