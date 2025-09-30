from flask import Flask, send_file, abort
import tempfile
import zipfile
import os
from capture import capture_elements, capture_multiple_units
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
        shutil.rmtree(tmp_dir, ignore_errors=True)
        pass

@app.post("/download_multiple_units")
def download_multiple_units():
    from flask import request
    data = request.json
    if not data or 'units' not in data:
        abort(400, "Missing 'units' in request body")

    units = data['units']
    if not isinstance(units, list) or not all(isinstance(u, str) for u in units):
        abort(400, "'units' must be a list of strings")

    url = "https://hcunits.net/units/"

    tmp_dir = tempfile.mkdtemp()
    try:
        capture_multiple_units(url, units, tmp_dir)

        zip_path = os.path.join(tmp_dir, "all_units_images.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in os.listdir(tmp_dir):
                if file.endswith(".png"):
                    zipf.write(os.path.join(tmp_dir, file), file)

        if not os.path.exists(zip_path):
            abort(500, "ZIP file was not created")

        return send_file(
            zip_path,
            mimetype="application/zip",
            as_attachment=True,
            download_name="all_units_images.zip",
        )

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        pass


if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000, debug=True)
