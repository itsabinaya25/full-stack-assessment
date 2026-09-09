from flask import Blueprint, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

from database import db


auth = Blueprint("auth", __name__)


# ===============================
# SIGNUP
# ===============================

@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        data = request.get_json()

        if not data:
            return {
                "success": False,
                "message": "Invalid request."
            }

        name = data.get("name", "").strip()
        age = data.get("age")
        address = data.get("address", "").strip()
        email = data.get("email", "").strip()
        mobile = data.get("mobile", "").strip()
        password = data.get("password", "")

        if not name or not age or not address or not email or not mobile or not password:
            return {
                "success": False,
                "message": "All fields are required."
            }

        if not str(age).isdigit():
            return {
                "success": False,
                "message": "Age must be a number."
            }

        age = int(age)

        if age < 1 or age > 120:
            return {
                "success": False,
                "message": "Please enter a valid age."
            }

        if "@" not in email or "." not in email:
            return {
                "success": False,
                "message": "Please enter a valid email address."
            }

        if not mobile.isdigit() or len(mobile) != 10:
            return {
                "success": False,
                "message": "Mobile number must contain exactly 10 digits."
            }

        if len(password) < 6:
            return {
                "success": False,
                "message": "Password must be at least 6 characters."
            }

        hashed_password = generate_password_hash(password)

        try:

            cursor = db.cursor()

            query = """
                INSERT INTO users
                (name, age, address, email, mobile, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                name,
                age,
                address,
                email,
                mobile,
                hashed_password
            )

            cursor.execute(query, values)
            db.commit()
            cursor.close()

            return {
                "success": True,
                "message": "Account created successfully"
            }

        except Exception as e:

            print("SIGNUP ERROR:", e)

            return {
                "success": False,
                "message": "Email may already be registered."
            }

    return render_template("signup.html")


# ===============================
# LOGIN
# ===============================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        data = request.get_json()

        if not data:
            return {
                "success": False,
                "message": "Invalid request."
            }

        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not email or not password:
            return {
                "success": False,
                "message": "Email and password are required."
            }

        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE email = %s"

        cursor.execute(query, (email,))

        user = cursor.fetchone()

        cursor.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return {
                "success": True,
                "message": "Login successful"
            }

        return {
            "success": False,
            "message": "Invalid email or password"
        }
    logout_message = request.args.get("logout")

    return render_template(
        "login.html",
        logout=logout_message
    )
    
      
@auth.route("/logout")
def logout():
    session.clear()
    return {
        "success":True,"message": "logged out successfully"
    }
# ===============================
# FORGOT PASSWORD
# ===============================

@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        data = request.get_json()

        if not data:
            return {
                "success": False,
                "message": "Invalid request."
            }

        email = data.get("email", "").strip()
        new_password = data.get("newPassword", "")

        if not email or not new_password:
            return {
                "success": False,
                "message": "Email and new password are required."
            }

        if len(new_password) < 6:
            return {
                "success": False,
                "message": "Password must be at least 6 characters."
            }

        cursor = db.cursor()

        query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(query, (email,))

        user = cursor.fetchone()

        if not user:
            cursor.close()

            return {
                "success": False,
                "message": "Email not registered."
            }

        hashed_password = generate_password_hash(new_password)

        update_query = """
            UPDATE users
            SET password = %s
            WHERE email = %s
        """

        cursor.execute(update_query, (hashed_password, email))
        db.commit()

        cursor.close()

        return {
            "success": True,
            "message": "Password reset successfully."
        }

    return render_template("forgot_password.html")
