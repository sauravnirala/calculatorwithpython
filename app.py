from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
csrf = CSRFProtect()
csrf.init_app(app) 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["GET"])
def add():
    a = float(request.args.get("a"))
    b = float(request.args.get("b"))
    return jsonify({"result": a + b})

@app.route("/sub", methods=["GET"])
def subtract():
    a = float(request.args.get("a"))
    b = float(request.args.get("b"))
    return jsonify({"result": a - b})

@app.route("/mul", methods=["GET"])
def multiply():
    a = float(request.args.get("a"))
    b = float(request.args.get("b"))
    return jsonify({"result": a * b})

@app.route("/div", methods=["GET"])
def divide():
    a = float(request.args.get("a"))
    b = float(request.args.get("b"))
    if b == 0:
        return jsonify({"error": "Division by zero"}), 400
    return jsonify({"result": a / b})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
