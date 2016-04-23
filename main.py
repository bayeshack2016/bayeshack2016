from flask import Flask
from flask import request
import json
import sys
import traceback
app = Flask(__name__)

@app.route("/")
def main():
    return "Hello World!"

@app.route('/webhook', methods=['GET', 'POST'])
def validate():
    try:
        if request.method == 'GET':
            return request.args.get('hub.challenge')
        else:
            if request.args.get('hub.verify_token') == 'verify_me':
                app.logger.error(request.args)
                app.logger.error(request.data)
                app.logger.error(request.form)
                app.logger.error(request.values)
                messaging_events = json.loads(request.data.decode("utf-8"))
                for i in xrange(len(messaging_events)):
                    event = messaging_events[i]
                    # sender = event.sender.id
                    if (event['message'] and event['message']['text']):
                        text = event['message']['text']
                        # Handle a text message from this sender
                        return text
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        app.logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))
        return 'Error, wrong validation token'

if __name__ == "__main__":
    app.run(debug=True)
