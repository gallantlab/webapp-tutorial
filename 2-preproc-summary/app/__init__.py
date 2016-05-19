from flask import Flask, request, render_template, send_from_directory
import logging
import os
import json
import numpy as np


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
        motdata = np.hstack(np.load(os.path.join(app.config['DATA_DIR'], 'motparams.npy')))
        data = [{'time': i,
                'x_trans': motdata[i, 0], 
                'y_trans': motdata[i, 1], 
                'z_trans': motdata[i, 2], 
                'x_rot': motdata[i, 3], 
                'y_rot': motdata[i, 4], 
                'z_rot': motdata[i, 5]}
                for i in range(motdata.shape[0])]
        return render_template('index.html', data = json.dumps(data))


    def get_motparams(expname, runnum):
        import docdb
        import numpy as np
        docdbi = docdb.getclient()
        mcims = docdbi.query(experiment_name = expname, generated_by_name="MotionCorrectFSL", block_number = runnum)
        motdata = mcims.generated_by.outputs["transforms"].get_params()
        return np.hstack(motdata)

    return app