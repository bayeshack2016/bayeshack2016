from flask import Flask
from flask import request
import sys
import traceback
app = Flask(__name__)

@app.route("/")
def main():
    return "Hello World!"

@app.route('/webhook', methods=['GET'])
def validate():
    try:
        if request.args.get('hub.verify_token') == 'verify_me':
            return request.args.get('hub.challenge')
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        app.logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))
    return 'Error, wrong validation token'

if __name__ == "__main__":
    app.run(debug=True)
