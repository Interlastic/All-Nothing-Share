from flask import Flask, send_from_directory, jsonify
import os
from flask import Response
import json
import time

app = Flask(__name__)

# === CONFIG ===
# Folder where your HTML/CSS/JS files live
STATIC_FOLDER = os.path.abspath("./static")  # Change if needed

@app.route('/')
def serve_root():
    return send_from_directory(STATIC_FOLDER, 'index.html')

@app.route('/<path:req_path>')
def serve_file_or_folder(req_path):
    full_path = os.path.join(STATIC_FOLDER, req_path)

    if os.path.isdir(full_path):
        # If the path is a directory, serve its index.html
        index_path = os.path.join(full_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(full_path, 'index.html')
        else:
            return send_from_directory(os.path.join(STATIC_FOLDER, "404"), 'index.html')

    elif os.path.isfile(full_path):
        # If the path is a file, serve it
        directory = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        return send_from_directory(directory, filename)

    else:
        return send_from_directory(os.path.join(STATIC_FOLDER, "404"), 'index.html')



@app.route('/items')
def stream_items():
    def generate():
        with open('./items.jsonl', 'r') as f:
            for line in f:
                yield line
                time.sleep(0.09)
    return Response(generate(), mimetype='application/x-ndjson')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)