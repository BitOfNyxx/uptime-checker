from flask import Flask

app = Flask(__name__)


@app.route("/")
def home() -> None:
    return "Uptime Checker"
