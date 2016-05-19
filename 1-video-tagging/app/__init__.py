from flask import Flask, request, render_template, send_from_directory
import logging
import os
import json


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

    @app.route('/')
    def index():
    	videos = os.listdir(app.config['VIDEO_DIR'])
    	video = [vid for vid in videos if allowed_file(vid)]
    	return render_template('index.html', video = video)

    @app.route('/video/<path:path>')
    def send_video(path):
    	return send_from_directory(app.config['VIDEO_DIR'], path)

    @app.route('/data/<path:path>')
    def show_data(path):
    	return send_from_directory(app.config['DATA_DIR'], path)


    @app.route('/submitted', methods = ['GET', 'POST'])
    def submit_message():
        video = [vid for vid in os.listdir('%s/' % app.config['VIDEO_DIR']) if vid.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']]
        tagged_video = {}
        form_data = request.form
        tags = form_data.getlist("tags")
        for i, vid in enumerate(video):
            tagged_video[vid] = {'humans': bool(form_data.get("humans"))}
            tagged_video[vid]['vehicles'] = bool(form_data.get("vehicles"))
            if tags[i] != '':
                tagged_video[vid]['tags'] = tags[i]

        if os.path.isfile(os.path.join(app.config['DATA_DIR'], app.config['DATA_FILE'])):
            with open(os.path.join(app.config['DATA_DIR'], app.config['DATA_FILE'])) as f:
                data = json.load(f)
            data.update(tagged_video)
        else:
            data = tagged_video

        with open(os.path.join(app.config['DATA_DIR'], app.config['DATA_FILE']), 'w') as f:
            json.dump(data, f, indent = 2, sort_keys=True)

        return 'Thank you for submitting the form! The tags are <a href="/data/%s">here</a>.' % (app.config['DATA_FILE'])

    return app