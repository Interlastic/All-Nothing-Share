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



items = [
    {"id": 0, "type": "app", "name": "Glyphify v3", "description": "By Fr4nKB - Advanced Glyph controls for notifications including an automatic music to Glyph composer. Supports Glyph Matrix on Phone (3)."},
    {"id": 1, "type": "app", "name": "SmartGlyph", "description": "By Experion Labs - Advanced Glyph notification control including Glyph Timer for Phone (1). Supports Glyph Matrix on Phone (3)."},
    {"id": 2, "type": "app", "name": "blockit", "description": "By Mirko_ddd - A tech detox phone blocking app with Glyph integration."},
    {"id": 3, "type": "app", "name": "Glyph Notifications", "description": "By GlyphLab - Advanced customisation for Glyph notifications."},
    {"id": 4, "type": "app", "name": "Simone", "description": "By RapidZapper - The classic memory game recreated with the Glyph interface."},
    {"id": 5, "type": "app", "name": "Glyph Compass", "description": "By JayKayCooperations - Use your Glyph interface as a compass."},
    {"id": 6, "type": "app", "name": "Noting", "description": "By Hearthborn - A Nothing styled notes and tasks app with cloud backup."},
    {"id": 7, "type": "app", "name": "nNotes", "description": "By Bhavuk Verma - An open source Nothing OS style notes app."},
    {"id": 8, "type": "app", "name": "Notes", "description": "By monospace - A Nothing styled notes app with built-in security."},
    {"id": 9, "type": "app", "name": "Dothing", "description": "By FirstYogi - A minimalist tasks app with cloud backup."},
    {"id": 10, "type": "app", "name": "No Things To Do List", "description": "By Martin Diermayr - A Nothing inspired task/to-do app and widget with customisable reminders."},
    {"id": 11, "type": "app", "name": "NoVolume", "description": "By NoAppsStudio - A fully customisable volume slider with Nothing aesthetic."},
    {"id": 12, "type": "app", "name": "NoCalendar", "description": "By NoAppsStudio - A calendar app inspired by Nothing design, with Google Calendar sync."},
    {"id": 13, "type": "app", "name": "N Dial", "description": "By Hearthborn - A Nothing styled phone dialer and contacts app."},
    {"id": 14, "type": "app", "name": "N Calc", "description": "By Hearthborn - A calculator with custom themes, including Nothing style."},
    {"id": 15, "type": "app", "name": "Battery Health", "description": "By monospace - A battery health monitoring app with design inspired by Nothing apps."},
    {"id": 16, "type": "app", "name": "Nothing Clock", "description": "By Sasha Chverenko - A Nothing style world clock, timer and stopwatch app."},
    {"id": 17, "type": "app", "name": "Noid", "description": "By TechSip Studios - A Nothing styled file management app."},
    {"id": 18, "type": "app", "name": "MissingCore Music", "description": "By MissingCore - A Nothing OS inspired, open source offline/local music player app."},
    {"id": 19, "type": "app", "name": "Widgets Pro", "description": "By Preethamkmr3 - Additional widgets inspired by Nothing design language."},
    {"id": 20, "type": "app", "name": "NothingLand", "description": "By TheGlitchh - An iOS style Dynamic Island for Nothing OS."},
    {"id": 21, "type": "app", "name": "Nothing News", "description": "By Mirko_ddd - All of the latest news from the Nothing community."},
    {"id": 22, "type": "app", "name": "Dot Battery", "description": "By RapidZapper - A live battery level wallpaper inspired by Nothing dot design language."}
]

@app.route('/items')
def stream_items():
    def generate():
        for item in items:
            yield json.dumps(item) + '\n'  # JSON line
            time.sleep(0.09)  # optional: slow down to simulate streaming
    return Response(generate(), mimetype='application/x-ndjson')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)