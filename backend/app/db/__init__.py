from .models import (
    Config,
    # LessonMembersAssoc,
    Group,
    Lesson,
    Member,
    Role,
    Topic,
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
    global_models = globals()
    if name in global_models:
        model = global_models.get(name)
        if issubclass(model, Config.BASE):
            return model
