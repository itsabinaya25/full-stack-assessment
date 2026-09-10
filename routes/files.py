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


# ==================== UPLOAD ====================

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
        user_name = secure_filename(
            session.get("user_name", "User")
        )

        uploaded_files = [
            request.files.get("file1"),
            request.files.get("file2")
        ]

        uploaded_count = 0
        duplicate_count = 0

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

            # Create filename
            filename = f"{user_name}_{extension}_{original_name}"

            # Check whether file already exists
            try:

                existing_files = (
                    supabase.storage
                    .from_("uploads")
                    .list()
                )

                file_exists = any(
                    item.get("name") == filename
                    for item in existing_files
                )

            except Exception as e:

                print("DUPLICATE CHECK ERROR:", repr(e))
                file_exists = False

            # If duplicate, skip it
            if file_exists:

                print("DUPLICATE FILE SKIPPED:", filename)
                duplicate_count += 1
                continue

            # Read file
            file_data = file.read()

            if not file_data:
                return jsonify({
                    "success": False,
                    "message": f"{original_name} is empty."
                })

            # Upload to Supabase Storage
            supabase.storage.from_("uploads").upload(
                filename,
                file_data,
                {
                    "content-type":
                        file.content_type
                        or "application/octet-stream"
                }
            )

            # Save metadata
            supabase.table("uploaded_files").insert({
                "filename": filename,
                "file_type": extension,
                "user_id": user_id
            }).execute()

            uploaded_count += 1

        # Nothing selected
        if uploaded_count == 0 and duplicate_count == 0:

            return jsonify({
                "success": False,
                "message": "Please select at least one file."
            })

        # Only duplicate files
        if uploaded_count == 0 and duplicate_count > 0:

            return jsonify({
                "success": False,
                "message": "File already exists. Duplicate file was not uploaded."
            })

        # Some uploaded + some duplicate
        if duplicate_count > 0:

            return jsonify({
                "success": True,
                "message":
                    f"{uploaded_count} file(s) uploaded. "
                    f"{duplicate_count} duplicate file(s) skipped."
            })

        # Normal upload
        return jsonify({
            "success": True,
            "message": f"{uploaded_count} file(s) uploaded successfully."
        })

    except Exception as e:

        print("UPLOAD ERROR:", repr(e))

        return jsonify({
            "success": False,
            "message": "Upload failed."
        }), 500


# ==================== DOWNLOAD ====================

@files.route("/download")
def download_file():

    try:

        file_name = request.args.get("filename")

        # Default test file
        if not file_name:
            file_name = "test_file.txt"

        # Download from Supabase Storage
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
                "Content-Disposition":
                    f'attachment; filename="{file_name}"'
            }
        )

    except Exception as e:

        print("DOWNLOAD ERROR:", repr(e))

        return jsonify({
            "success": False,
            "message": "File not found."
        }), 404