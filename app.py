from flask import Flask, request, jsonify, render_template
from flask_wtf.csrf import CSRFProtect
import os

# Prometheus imports

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(**name**, template_folder=os.path.join(os.path.dirname(os.path.abspath(**file**)), 'templates'))
csrf = CSRFProtect()
csrf.init_app(app)

# Metrics

REQUEST_COUNT = Counter('app_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
ERROR_COUNT = Counter('app_errors_total', 'Total Errors')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency')

@app.before_request
def before_request():
request.start_time = REQUEST_LATENCY.time()

@app.after_request
def after_request(response):
REQUEST_COUNT.labels(request.method, request.path).inc()
request.start_time.observe_duration()
return response

# Metrics endpoint (IMPORTANT)

@app.route("/metrics")
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
return jsonify({"error": "Invalid input"}), 400

@app.route("/sub", methods=["GET"])
def subtract():
try:
a = float(request.args.get("a"))
b = float(request.args.get("b"))
return jsonify({"result": a - b})
except:
ERROR_COUNT.inc()
return jsonify({"error": "Invalid input"}), 400

@app.route("/mul", methods=["GET"])
def multiply():
try:
a = float(request.args.get("a"))
b = float(request.args.get("b"))
return jsonify({"result": a * b})
except:
ERROR_COUNT.inc()
return jsonify({"error": "Invalid input"}), 400

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
return jsonify({"error": "Invalid input"}), 400

if **name** == "**main**":
app.run(host="0.0.0.0", port=5000)
