from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
    return "Hello World!"

@app.route('/webhook', methods=['GET'])
def validate(req, res):
    if req.query['hub.verify_token'] == 'verify_me':
        res.send(req.query['hub.challenge']);
    res.send('Error, wrong validation token');

if __name__ == "__main__":
    app.run()
