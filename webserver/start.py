import os
import sys

import dotenv
import uvicorn

dotenv.load_dotenv(dotenv.find_dotenv('env.dev'))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from webserver.settings import DEBUG
    sys.path.append(BASE_DIR)
    os.chdir(os.path.dirname(BASE_DIR))
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
