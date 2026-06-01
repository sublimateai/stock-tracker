from src.load_config import load_server_config
from src.server.web.main import app
import uvicorn

server_config = load_server_config()


def main():
    uvicorn.run(app, **server_config.get("uvicorn", {"port": 8080, "host": "0.0.0.0"}))


if __name__ == "__main__":
    main()
