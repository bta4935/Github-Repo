import os
import uuid
import subprocess
import zipfile
import threading
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DOCS_BASE = r"c:\Users\2 9ice\Desktop\github-repo-understand\docs"

# Global job status store
job_status = {}  # job_id: {status, progress, output_dir, error}

def run_cli_and_generate(url, job_id=None):
    run_id = job_id if job_id else str(uuid.uuid4())
    out_dir = os.path.join(DOCS_BASE, run_id)
    os.makedirs(out_dir, exist_ok=True)
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    MAIN_PY = os.path.join(PROJECT_ROOT, "main.py")
    cmd = ["python", MAIN_PY, "--repo", url, "-o", out_dir]
    try:
        # Optionally, update progress here (if you want more granular progress)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(result.stderr)
        return out_dir, None
    except Exception as e:
        return None, str(e)

def zip_output_folder(folder_path):
    zip_path = f"{folder_path}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, folder_path)
                zipf.write(abs_path, rel_path)
    return zip_path

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data.get("github_url")
    if not url:
        return jsonify({"error": "No GitHub URL provided"}), 400
    job_id = str(uuid.uuid4())
    job_status[job_id] = {"status": "in_progress", "progress": 0, "output_dir": None, "error": None}

    def background_job():
        job_status[job_id]["progress"] = 0  # Start
        out_dir, error = run_cli_and_generate(url, job_id=job_id)
        if error:
            job_status[job_id]["status"] = "error"
            job_status[job_id]["error"] = error
            job_status[job_id]["progress"] = -1
        else:
            job_status[job_id]["progress"] = 50  # CLI finished
            # Zip the output
            zip_output_folder(out_dir)
            job_status[job_id]["status"] = "done"
            job_status[job_id]["output_dir"] = out_dir
            job_status[job_id]["download_url"] = f"/download?dir={os.path.basename(out_dir)}"
            job_status[job_id]["progress"] = 100

    thread = threading.Thread(target=background_job)
    thread.start()
    return jsonify({"job_id": job_id, "status": "in_progress"})

@app.route("/download")
def download():
    dir_name = request.args.get("dir")
    folder_path = os.path.join(DOCS_BASE, dir_name)
    zip_path = f"{folder_path}.zip"
    if not os.path.exists(zip_path):
        zip_output_folder(folder_path)
    return send_file(zip_path, as_attachment=True)

@app.route("/status", methods=["GET"])
def status():
    job_id = request.args.get("job_id")
    if not job_id or job_id not in job_status:
        return jsonify({"error": "Invalid or missing job_id"}), 400
    status_info = job_status[job_id].copy()
    # Optionally, do not return output_dir path for security
    return jsonify(status_info)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
