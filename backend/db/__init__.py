from .models import Config


Config.BASE.metadata.create_all(Config.ENGINE)
