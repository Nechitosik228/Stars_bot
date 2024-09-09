import secrets
from quart import Quart
from quart_auth import QuartAuth


class AppConfig:
    def __init__(
        self,
        name: str,
        app: Quart = Quart(__name__),
        auth: QuartAuth = QuartAuth(),
        secret_key: str = secrets.token_urlsafe(64),
        host: str | None = None,
        port: int | None = None,
        debug: bool | None = None,
    ) -> None:
        self.app = app or Quart(name)
        self.app.secret_key = secret_key
        self.auth = auth

        self.host = host
        self.port = port
        self.debug = debug

        self.auth.init_app(app=self.app)
