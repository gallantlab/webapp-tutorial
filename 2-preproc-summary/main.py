import app
import config

preproc_app = app.create_app(config)

if __name__ == '__main__':
	preproc_app.run(host='127.0.0.1', port=8081, debug=True)