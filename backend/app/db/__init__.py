from .models import (
    Config,
    LessonMember,
    Group,
    Lesson,
    Member,
    Role,
    Topic,
    DB_MODELS,
)


def up():
    Config.BASE.metadata.create_all(Config.ENGINE)


def down():
    Config.BASE.metadata.drop_all(Config.ENGINE)


def migrate():
    down()
    up()


def get_db():
    db = Config.SESSION()
    try:
        yield db
    finally:
        db.close()


def get_model(name: str = "") -> type | None:
    print(name)
    db_models = DB_MODELS

    if name in db_models:
        
        model = db_models.get(name)
        if issubclass(model, Config.BASE):
            return model
