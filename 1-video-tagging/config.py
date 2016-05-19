# Statement for enabling the development environment
DEBUG = True

# Define directories
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

VIDEO_DIR = os.path.join(BASE_DIR, 'video')
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_FILE = "tagged.json"

ALLOWED_EXTENSIONS = set(['mp4', 'ogv'])