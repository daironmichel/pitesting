import os


DEBUG = os.getenv('DEBUG', 'False') == 'True'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
