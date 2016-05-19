import app
import config

log_app = app.create_app(config)

if __name__ == '__main__':
	log_app.run(host='127.0.0.1', port=8082, debug=True)