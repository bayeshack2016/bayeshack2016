from flask import Flask
from flask import request
import json
import requests
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
            if request.args.get('hub.verify_token') == 'verify_me':
                return request.args.get('hub.challenge')
        else:
            sys.stderr.write('stderr\n')
            sys.stdout.write('stdout\n')
            app.logger.error(request.args)
            app.logger.error(request.data)
            app.logger.error(request.form)
            app.logger.error(request.values)
            messaging_events = json.loads(request.data.decode("utf-8"))
            messages = messaging_events['entry'][0]['messaging']
            sys.stderr.write(str(messaging_events) + '\n')
            for event in messages:
                # sender = event.sender.id
                if (event.get('message') and event['message']['text']):
                    sender_id = event['sender']['id']
                    text = event['message']['text']
                    # Handle a text message from this sender
                    sys.stderr.write(text + '\n')
                    sys.stderr.write(str(sender_id) + '\n')
                    sendTextMessage(sender_id, text)
                    return text
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        app.logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))
        return 'Error, wrong validation token'

def sendTextMessage(sender, text):
    token = "CAAYM4P71Md8BAMRPqQyRa7pHVvQyXydWi2LRzZBVoZBPr8qxhLi9ZC1kD26PgFx3IB1E17tTjECLFGn4uerwISpVzuLMmqIaGSgvyMNgF0ix1RZA4x1VGPiKMXCRzJ1B7xH2D2G0fuHGeAroC4gVX8qqxz2aaTbusYz5P82arcy4oV6ZAScwKcZBWfcMauYpUZD"
    url = "https://graph.facebook.com/v2.6/me/messages"
    payload = dict(recipient=dict(id=sender), message=text, qs=dict(access_token=token))
    r = requests.post(url, data=payload)
    sys.stderr.write(str(r.status_code) + '\n')


# def sendTextMessage(sender, text):
#     messageData = {text=text}
#     request({
#         url: 'https://graph.facebook.com/v2.6/me/messages',
#         qs: {access_token:token},
#         method: 'POST',
#         json: {
#         recipient: {id:sender},
#         message: messageData,
#         }
#     }, function(error, response, body) {
#         if (error) {
#         console.log('Error sending message: ', error);
#         } else if (response.body.error) {
#         console.log('Error: ', response.body.error);
#         }
#     });
#     }

if __name__ == "__main__":
    app.run(debug=True)
