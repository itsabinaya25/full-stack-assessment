
from flask import Blueprint, request, session, jsonify
from werkzeug.utils import secure_filename
from database import supabase

files = Blueprint("files", __name__)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@files.route("/upload", methods=["POST"])
def upload_files():
    try:
        # Check login
        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Please login first."
            })

        user_id = session["user_id"]
        user_name = secure_filename(session.get("user_name", "User"))

        uploaded_files = [
            request.files.get("file1"),
            request.files.get("file2")
        ]

        uploaded_count = 0

        for file in uploaded_files:

            # Skip empty file fields
            if not file or not file.filename:
                continue

            # Check extension
            if not allowed_file(file.filename):
                return jsonify({
                    "success": False,
                    "message": "Only PDF, PNG, JPG, and JPEG files are allowed."
                })

            # Clean original filename
            original_name = secure_filename(file.filename)

            # Get extension
            extension = original_name.rsplit(".", 1)[1].lower()

            # Create unique filename using logged-in user's name
            filename = f"{user_name}_{extension}_{original_name}"

            # Read uploaded file into memory
            file_data = file.read()

            if not file_data:
                return jsonify({
                    "success": False,
                    "message": f"{original_name} is empty."
                })

            # Upload to Supabase Storage
            response = (
                supabase.storage
                .from_("uploads")
                .upload(
                    filename,
                    file_data,
                    {
                        "content-type": file.content_type or "application/octet-stream"
                    }
                )
            )

            print("STORAGE UPLOAD RESPONSE:", response)

            # Save file metadata in Supabase database
            supabase.table("uploaded_files").insert({
                "filename": filename,
                "file_type": extension,
                "user_id": user_id
            }).execute()

            uploaded_count += 1

        # No files selected
        if uploaded_count == 0:
            return jsonify({
                "success": False,
                "message": "Please select at least one file."
            })

        return jsonify({
            "success": True,
            "message": "Files uploaded successfully."
        })

    except Exception as e:
        print("UPLOAD ERROR:", repr(e))

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@files.route("/download")
def download_file():
    try:
        file_name = request.args.get("filename")

        if not file_name:
            file_name = "test_file.txt"

        file_data = (
            supabase.storage
            .from_("uploads")
            .download(file_name)
        )

        return (
            file_data,
            200,
            {
                "Content-Type": "application/octet-stream",
                "Content-Disposition": f'attachment; filename="{file_name}"'
            }
        )

    except Exception as e:
        print("DOWNLOAD ERROR:", repr(e))

        return jsonify({
            "success": False,
            "message": "File not found."
        }), 404

