from flask import Flask, request, render_template, send_from_directory, jsonify
import logging
import os

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


	@app.route("/", methods=["GET", "POST"])
	def logform():
		return render_template('index.html') #, sequences = sequences)

	@app.route("/export", methods=["GET", "POST"])
	def exportform():
		form = request.form
		form_template = '''
		[Subject]\n\n
		%s\n\n
		[Operator]\n\n
		%s\n\n
		[Notes]\n\n
		%s\n\n
		[Runs]\n\n
		%s
		'''
		run_template = '''
		%s:%s:%s:%s #%s
		'''
		runnums = form.getlist('runnum')
		sequences = form.getlist('sequence')
		stimuli = form.getlist('stimuli')
		trnums = form.getlist('trnum')
		runnotes = form.getlist('runnotes')
		runs = "\n".join([run_template % (runnums[i], sequences[i], stimuli[i], trnums[i], runnotes[i]) for i in range(len(runnums))])

		form_filled = form_template % (form['subject'], form['operator'], form['notes'], runs)
		return jsonify(text=form_filled)

	return app