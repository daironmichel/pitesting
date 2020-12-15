import os
import uvicorn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    uvicorn.run(
        "webserver.app:app",
        host="127.0.0.1",
        port=5000,
        log_level="debug",
        env_file=f"{BASE_DIR}/webserver/env.dev",
        reload=True
    )
