from flask import Flask, send_file, abort
import tempfile
import zipfile
import os
from capture import capture_elements
import shutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.post("/download_images/<unit_id>")
def download_images(unit_id):
    url = f"https://hcunits.net/units/{unit_id}/"

    tmp_dir = tempfile.mkdtemp()
    try:
        files = capture_elements(url, tmp_dir, unit_id)
        if not files:
            abort(404, "No elements found")

        zip_path = os.path.join(tmp_dir, f"{unit_id}_images.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in files:
                zipf.write(file, os.path.basename(file))

        return send_file(
            zip_path,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"{unit_id}_images.zip"
        )

    finally:
        # Optional: clean up temp directory after sending (Flask should copy the file first)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        pass



if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000, debug=True)
