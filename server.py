from flask import Flask, send_from_directory, jsonify
import os

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

items = [
    {"id": 0, "type": "app", "name": "CoolApp", "description": "A cool app to do cool things."},
    {"id": 1, "type": "ringtone", "name": "Classic Ringtone", "description": "A classic ringtone sound."},
    {"id": 2, "type": "app", "name": "GameFun", "description": "An addictive mobile game."}
]

@app.route('/items')
def get_items():
    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True, port=5000)