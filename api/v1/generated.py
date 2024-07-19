from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.connection import get_db_sessionmaker
from database.controllers.generated import update_app_json
from schemas.v1.app import AppOperationOK
from schemas.v1.generated import Person

router = APIRouter()


@router.post("/{kind}/{app_id}")
async def save_json_handler(
    db_sessionmaker: Annotated[async_sessionmaker, Depends(get_db_sessionmaker)],
    kind: str,
    app_id: UUID,
    new_json: Person,
) -> AppOperationOK:
    return await update_app_json(
        db_sessionmaker=db_sessionmaker,
        kind=kind,
        app_id=app_id,
        new_json=new_json,
    )
    