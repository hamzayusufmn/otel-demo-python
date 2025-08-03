import datetime
import flask
import logging
import time
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

app = flask.Flask(__name__)
start = datetime.datetime.now()

# Disable default werkzeug request logging
log = logging.getLogger("werkzeug")
log.disabled = True

@app.route('/', methods=['GET'])
def root():
    logging.warning('main route was accessed')
    return flask.jsonify({'message': 'flask app root/'}), 200

@app.route('/health', methods=['GET'])
def health():
    now = datetime.datetime.now()
    logging.warning("health route was accessed")
    return flask.jsonify({'message': f'up and running since {(now - start)}'})


def stiumlate_db_lookup():
    with tracer.start_as_current_span("db_lookup"):
        time.sleep(3) # will show db delay
        logging.warning('db lookup finshed')


@app.route('/slow', methods=['GET'])
def slow():
    logging.warning("slow route was accessed, delay will be stimulated")
    stiumlate_db_lookup()
    time.sleep(10)
    logging.warning("responding after 10 second delay" )

    return flask.jsonify({"message": f"slow response after 10 seconds"}), 200


@app.route('/error', methods=['GET'])
def error():
    with tracer.start_as_current_span("error_simulation") as span:
        logging.error("Simulating an internal server error")
        raise Exception("Intentional 500 error for tracing/logging demo")

@app.errorhandler(404)
def page_not_found(error):
    logging.error(f"404 error: {error}")
    return flask.jsonify({'message': 'route not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
