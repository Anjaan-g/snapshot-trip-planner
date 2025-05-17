from flask import Flask, jsonify
from flask_cors import CORS
from models.file_metadata import init_db
from routes.random import random_bp
from routes.upload import upload_bp

app = Flask(__name__)

CORS(app)
init_db()
app.register_blueprint(random_bp)
app.register_blueprint(upload_bp)


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
