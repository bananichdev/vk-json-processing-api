from settings import CONTROLLER_PATH, REST_PATH
from utils.json_parser import parse_json


def generate_controller(model_name: str) -> str:
    return (
        f"""from uuid import UUID

from sqlalchemy import and_, update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.controllers.app import get_app
from database.models import AppModel
from schemas.v1.app import AppOperationOK
from schemas.v1.errors import DBAPICallError
from schemas.v1.generated import {model_name}


async def update_app_json(
    db_sessionmaker: async_sessionmaker,
    kind: str,
    app_id: UUID,
    new_json: {model_name},
) -> AppOperationOK:
    await get_app(
        db_sessionmaker=db_sessionmaker,
        kind=kind,
        app_id=app_id,
    )

    try:
        async with db_sessionmaker.begin() as session:
            await session.execute(
                update(AppModel)
                .where(and_(AppModel.kind == kind, AppModel.app_id == app_id))
                .values(json=new_json.dict())
            )
    except DBAPIError as e:
        raise DBAPICallError(
            msg=f"can not save json to app with kind="""
        + """{kind} and app_id={app_id}"
        ) from e

    return AppOperationOK(kind=kind, app_id=app_id)
    """
    )


def generate_rest(model_name: str) -> str:
    return (
        f"""from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.connection import get_db_sessionmaker
from database.controllers.generated import update_app_json
from kafka import send_message
from schemas.v1.app import AppOperationOK
from schemas.v1.generated import {model_name}

router = APIRouter()"""
        + """


@router.post("/{kind}/{app_id}")"""
        + f"""
async def save_json_handler(
    db_sessionmaker: Annotated[async_sessionmaker, Depends(get_db_sessionmaker)],
    kind: str,
    app_id: UUID,
    new_json: {model_name},
) -> AppOperationOK:""" + """
    response = await update_app_json(
        db_sessionmaker=db_sessionmaker,
        kind=kind,
        app_id=app_id,
        new_json=new_json,
    )

    await send_message(
        topic="app_updates",
        key=str(app_id),
        value={
            "event": "json saved",
            "kind": kind,
            "app_id": str(app_id),
            "new_json": new_json.dict(),
        },
    )

    return response
    """
    )


def main():
    schema = parse_json()

    print(f"Генерация контроллеров базы данных в {CONTROLLER_PATH} ...")
    with open(CONTROLLER_PATH, "w") as f:
        f.write(generate_controller(schema["title"]))
    print("Генерация прошла успешно!")

    print(f"Генерация контроллеров REST приложения в {REST_PATH} ...")
    with open(REST_PATH, "w") as f:
        f.write(generate_rest(schema["title"]))
    print("Генерация прошла успешно!")


if __name__ == "__main__":
    main()
