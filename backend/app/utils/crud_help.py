from pydantic import BaseModel, Field, create_model
from sqlalchemy import MetaData
from loguru import logger
from typing import Type, TypeVar
from typing import Dict, List, Tuple
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from ..db import get_db, get_model
from loguru import logger

T = TypeVar("T", bound=BaseModel)


def schema_factory(
    schema_cls: Type[T], pk_field_name: str = "id", name: str = "Create"
) -> Type[T]:
    """
    Is used to create a CreateSchema which does not contain pk
    """

    fields = {
        name: (f.annotation, ...)
        for name, f in schema_cls.model_fields.items()
        if name != pk_field_name
    }

    name = schema_cls.__name__ + name
    schema: Type[T] = create_model(name, **fields)  # type: ignore
    return schema


def generate_model(
    name: str,
    inheritanced: Tuple[type],
    fields: Dict[str, type] = {},
    inner_classes: List[type] = [],
) -> type:
    model_fields = fields.copy()
    model = type(name, inheritanced, {})
    for field, type_ in model_fields.items():
        setattr(model, field, Field())
    for inner_cls in inner_classes:
        setattr(model, inner_cls.__name__, inner_cls)
    model.__annotations__ = model_fields

    return model


@logger.catch
def generate_pydantic_models(
    meta: MetaData,
    create_postfix: str = "Create",
    update_postfix: str = "Update",
    base_postfix: str = "Base",
    base_model_exclude_columns: List[str] = [
        "id",
    ],
    exclude_tables: List[str] = [],
) -> List[Type]:
    "Function to generate Pydantic models from SQLAlchemy metadata"
    pydantic_models = []

    for name, model in meta.tables.items():

        if model in exclude_tables or name in exclude_tables:
            continue
        cls_name = "".join([n.title() for n in name.split("_")])
        pydantic_model = {"name": str(cls_name)}
        # parse columns in Base model
        columns = list(
            filter(
                lambda col: col.name not in base_model_exclude_columns, model.columns
            )
        )

        create_annotations = {}
        for column in model.columns:
            create_annotations[column.name] = column.type.python_type

        model_annotations = {}
        for column in columns:
            model_annotations[column.name] = column.type.python_type

        inner_cls = type("Config", (), {})
        inner_cls.orm_mode = True
        update_annotations = dict(create_annotations, **model_annotations)

        base = generate_model(
            name=f"{cls_name}Base",
            inheritanced=(BaseModel,),
            fields=create_annotations,
        )
        model_create = generate_model(
            name=f"{cls_name}{create_postfix}",
            inheritanced=(base,),
            fields=create_annotations,
        )
        model_update = generate_model(
            name=f"{cls_name}{update_postfix}",
            inheritanced=(model_create,),
            fields=update_annotations,
            inner_classes=[
                inner_cls,
            ],
        )
        model_base = generate_model(
            name=f"{cls_name}{base_postfix}",
            inheritanced=(model_create,),
            fields=model_annotations,
            inner_classes=[
                inner_cls,
            ],
        )
        # pydantic_model["base"] = base
        pydantic_model["base_schema"] = schema_factory(model_base)
        pydantic_model["update_schema"] = schema_factory(model_update)
        pydantic_model["create_schema"] = schema_factory(model_create)
        pydantic_models.append(pydantic_model)

    return pydantic_models


@logger.catch
def generate_crud_routers(pydantic_models: list) -> list[SQLAlchemyCRUDRouter]:
    crud_routers = []
    for model in pydantic_models:
        
        name = model.get("name")
        base_schema = model.get("base_schema")
        update_schema = model.get("update_schema")
        create_schema = model.get("create_schema")
        model = get_model(name)

        if model:
            print(model)
            router = SQLAlchemyCRUDRouter(
                schema=base_schema,
                create_schema=create_schema,
                update_schema=update_schema,
                db_model=model,
                db=get_db,
                prefix=name,
            )
            crud_routers.append(router)
    return crud_routers
