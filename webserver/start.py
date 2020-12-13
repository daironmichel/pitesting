import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "webserver.app:app",
        host="127.0.0.1",
        port=5000,
        log_level="debug",
        env_file="./webserver/env.dev",
        reload=True
    )
