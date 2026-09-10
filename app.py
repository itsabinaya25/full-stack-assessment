from flask import Flask, render_template, send_from_directory, session, redirect
from flask_cors import CORS

from routes.auth import auth
from routes.files import files
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True
)

app.register_blueprint(auth)
app.register_blueprint(files)

# CORS will be configured with the frontend Render URL
CORS(
    app,
    origins=["https://full-stack-assessment-frontend.onrender.com"],
    supports_credentials=True
)


@app.route("/styles/<path:filename>")
def styles(filename):
    return send_from_directory("styles", filename)


@app.route("/")
def home():
    return render_template("signup.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user_name=session.get("user_name", "User")
    )

@app.route("/current-user")
def current_user():

    if "user_id" not in session:
        return {
            "success": False,
            "message": "User not logged in"
        }, 401

    return {
        "success": True,
        "user_name": session.get("user_name", "User")
    }


if __name__ == "__main__":
    app.run(debug=True)

    