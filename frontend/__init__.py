if __name__ == "__main__":
    from config import AppConfig
else:
    from .config import AppConfig

app_config = AppConfig(__name__)

if __name__ == "__main__":
    import routes
else:
    from . import routes


def run() -> None:
    app_config.app.run()
