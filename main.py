from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
    return "Hello World!"

@app.route('/webhook', methods=['GET'])
def validate():
    if request.query['hub.verify_token'] == 'verify_me':
        return request.query['hub.challenge']
    return 'Error, wrong validation token'

if __name__ == "__main__":
    app.run()
