from flask import Flask, render_template, send_from_directory, session, redirect, request
from routes.auth import auth
from routes.files import files
from routes.files import files
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth)
app.register_blueprint(files)

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

if __name__ == "__main__":
    app.run(debug=True)
