from flask import Flask
from flask import json
import logging

app = Flask(__name__)

@app.route('/status')
def status():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info('Main request successfull')
    return response

@app.route('/metrics')
def metrics():
    response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"UserCount":140,"UserCountActive":23}}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info('Main request successfull')
    return response

@app.route("/")
def hello():
    return "Hello World!"
    app.logger.info('Main request successfull')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    # Stream logs to a file, and set the default log level to DEBUG
    app.run(host='0.0.0.0')
