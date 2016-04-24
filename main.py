from flask import Flask
from flask import request
# from rq import Queue
# from worker import conn
import json
import sys
import traceback
from worker import store_response

app = Flask(__name__)

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



def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
