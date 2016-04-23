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
    token = "CAAYM4P71Md8BAL1BzNrSPZCHnbZAVjvmfJwI4KSdFDRXxREVLUfacPKGP05GA82LGYkZCMDYXPb09k4yV04Rv8b0xtOXtj3aqFZA8ApW8D4v8zvuIbNHsJ4ydXsLq8XxKDTt0xgVnvrQTe44ArduAZARQ2YwAYEZAJhzs29oQjtExRvRup3ZACyhZCSj4EoZBKi4ZD"
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
            messages = messaging_events['entry']['messaging']
            sys.stderr.write(str(messaging_events) + '\n')
            for i in xrange(len(messages)):
                event = messages[i]
                # sender = event.sender.id
                if (event['message'] and event['message']['text']):
                    text = event['message']['text']
                    # Handle a text message from this sender
                    sys.stderr.write(text + '\n')
                    return text
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        app.logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))
        return 'Error, wrong validation token'

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
