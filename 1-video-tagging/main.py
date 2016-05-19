import app
import config

label_app = app.create_app(config)

if __name__ == '__main__':
	label_app.run(host='127.0.0.1', port=8080, debug=True)