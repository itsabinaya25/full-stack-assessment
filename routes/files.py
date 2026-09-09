from flask import Blueprint, request, session, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os

from database import db


files = Blueprint("files", __name__)


ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ===============================
# FILE UPLOAD
# ===============================

@files.route("/upload", methods=["POST"])
def upload_files():

    try:

        if "user_id" not in session:
            return {
                "success": False,
                "message": "Please login first."
            }

        user_name = secure_filename(
            session.get("user_name", "User")
        )

        uploaded_files = [
            request.files.get("file1"),
            request.files.get("file2")
        ]

        cursor = db.cursor()

        for file in uploaded_files:

            if file and allowed_file(file.filename):

                original_name = secure_filename(file.filename)

                extension = original_name.rsplit(
                    ".", 1
                )[1].lower()

                filename = f"{user_name}_{extension}_{original_name}"

                file.save(
                    os.path.join(
                        current_app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )

                # Store file metadata in MySQL
                cursor.execute(
                    """
                    INSERT INTO uploaded_files
                    (filename, file_type, user_id)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        filename,
                        extension,
                        session["user_id"]
                    )
                )

            elif file:

                cursor.close()

                return {
                    "success": False,
                    "message": "Only PDF, PNG, JPG, and JPEG files are allowed."
                }

        db.commit()

        cursor.close()

        return {
            "success": True,
            "message": "Files uploaded successfully."
        }

    except Exception as e:

        print("UPLOAD ERROR:", e)

        return {
            "success": False,
            "message": str(e)
        }, 500


# ===============================
# FILE DOWNLOAD
# ===============================

@files.route("/download")
def download_file():

    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        "test_file.txt",
        as_attachment=True
    )