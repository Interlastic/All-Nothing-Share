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
                print(line)
    return Response(generate(), mimetype='application/x-ndjson')

@app.route('/Phone<phone_id>')
def serve_phone(phone_id):
    # read our template file
    with open(os.path.join(STATIC_FOLDER, 'templates/phonetemplate.html'), 'r') as f:
        template = f.read()
    
    # replace placeholders based on phone_id
    phone_data = get_phone_data(phone_id)  # ur function to get data
    
    html = template.replace('{{PHONE_NAME}}', phone_data['name'])
    html = html.replace('{{PHONE_NAMENOSPACE}}', phone_data['name'].replace(' ', ''))

    #  Now we replace everything for otherphone
    for i in range(1, 5):
        other_phone_key = f'otherphone{i}'
        if other_phone_key in phone_data:
            html = html.replace(f'{{{{OTHER_PHONE{i}}}}}', phone_data[other_phone_key])
        else:
            html = html.replace(f'{{{{OTHER_PHONE{i}}}}}', 'Unknown')
    # We also need to replace the "href"s so we need to take otherphone{i} like before but remove spaces. so if otherphone1 is Phone 2 we write Phone2 .
    for i in range(1, 5):
        other_phone_key = f'otherphone{i}'
        if other_phone_key in phone_data:
            phone_name = phone_data[other_phone_key]
            phone_href = phone_name.replace(' ', '')
            html = html.replace(f'{{{{OTHERPHONE{i}_HREF}}}}', f'/{phone_href}')

    return html

def get_phone_data(phone_id):
    # return dict w phone info based on id
    phones = {
   '1': {'name': 'Phone 1', 'otherphone1': 'Phone 2', 'otherphone2': 'Phone 2a', 'otherphone3': 'Phone 3a', 'otherphone4': 'Phone 3', 'desc': 'test'},
   '2': {'name': 'Phone 2', 'otherphone1': 'Phone 1', 'otherphone2': 'Phone 2a', 'otherphone3': 'Phone 3a', 'otherphone4': 'Phone 3', 'desc': 'test'},
   '2a': {'name': 'Phone 2a', 'otherphone1': 'Phone 1', 'otherphone2': 'Phone 2', 'otherphone3': 'Phone 3a', 'otherphone4': 'Phone 3', 'desc': 'test'},
   '3a': {'name': 'Phone 3a', 'otherphone1': 'Phone 1', 'otherphone2': 'Phone 2', 'otherphone3': 'Phone 2a', 'otherphone4': 'Phone 3', 'desc': 'test'},
   '3': {'name': 'Phone 3', 'otherphone1': 'Phone 1', 'otherphone2': 'Phone 2', 'otherphone3': 'Phone 2a', 'otherphone4': 'Phone 3a', 'desc': 'test'},
    }
    return phones.get(phone_id, {'name': 'Unknown', 'desc': 'Not found'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)