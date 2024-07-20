from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.connection import get_db_sessionmaker
from database.controllers.generated import update_app_json
from kafka import send_message
from schemas.v1.app import AppOperationOK
from schemas.v1.generated import Document

router = APIRouter()


@router.post("/{kind}/{app_id}")
async def save_json_handler(
    db_sessionmaker: Annotated[async_sessionmaker, Depends(get_db_sessionmaker)],
    kind: str,
    app_id: UUID,
    new_json: Document,
) -> AppOperationOK:
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
    