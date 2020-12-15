import os
import sys
import uvicorn

DEBUG = os.getenv('DEBUG', 'False') == 'True'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(BASE_DIR))

if __name__ == "__main__":
    uvicorn.run(
        "webserver.app:app",
        host="127.0.0.1" if DEBUG else "0.0.0.0",
        port=5000 if DEBUG else 80,
        log_level="debug" if DEBUG else "info",
        debug=DEBUG,
        root_path=BASE_DIR,
        env_file=f"{BASE_DIR}/webserver/env.dev",
        reload=DEBUG
    )
