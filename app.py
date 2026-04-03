from flask import Flask, request, jsonify, render_template
from flask_wtf.csrf import CSRFProtect
import os , time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
csrf = CSRFProtect()
csrf.init_app(app)
app.config['WTF_CSRF_ENABLED'] = False

INVALID_INPUT_MSG = "Invalid input"

# Metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
ERROR_COUNT = Counter('app_errors_total', 'Total Errors')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency')

@app.before_request
def before_request():
    request.start_time = time.time()  # plain float, not a Timer object

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(request.method, request.path).inc()
    duration = max(time.time() - request.start_time, 0)
    REQUEST_LATENCY.observe(duration)  # manually record the duration
    return response

@app.route("/metrics", methods=["GET"])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/add", methods=["GET"])
def add():
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
        return jsonify({"result": a + b})
    except:
        ERROR_COUNT.inc()
        return jsonify({"error": INVALID_INPUT_MSG}), 400

@app.route("/sub", methods=["GET"])
def subtract():
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
        return jsonify({"result": a - b})
    except:
        ERROR_COUNT.inc()
        return jsonify({"error": INVALID_INPUT_MSG}), 400

@app.route("/mul", methods=["GET"])
def multiply():
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
        return jsonify({"result": a * b})
    except:
        ERROR_COUNT.inc()
        return jsonify({"error": INVALID_INPUT_MSG}), 400

@app.route("/div", methods=["GET"])
def divide():
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
        if b == 0:
            ERROR_COUNT.inc()
            return jsonify({"error": "Division by zero"}), 400
        return jsonify({"result": a / b})
    except:
        ERROR_COUNT.inc()
        return jsonify({"error": INVALID_INPUT_MSG}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
