from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.connection import get_db_sessionmaker
from database.controllers.app import delete_app, get_app, update_app_state
from kafka import send_message
from schemas.v1.app import App, AppOperationOK, AppState
from settings import update_configuration

router = APIRouter()


@router.get("/{kind}/{app_id}", status_code=status.HTTP_200_OK)
async def get_app_handler(
    db_sessionmaker: Annotated[async_sessionmaker, Depends(get_db_sessionmaker)],
    kind: str,
    app_id: UUID,
) -> App:
    """Return app"""
    return await get_app(
        db_sessionmaker=db_sessionmaker,
        kind=kind,
        app_id=app_id,
    )


@router.get("/{kind}/{app_id}/state", status_code=status.HTTP_200_OK)
async def get_app_state_handler(
    db_sessionmaker: Annotated[async_sessionmaker, Depends(get_db_sessionmaker)],
    kind: str,
    app_id: UUID,
) -> AppState:
    """Return app state"""
    app = await get_app(
        db_sessionmaker=db_sessionmaker,
        kind=kind,
        app_id=app_id,
    )
    return AppState(state=app.state)


@router.put("/{kind}/{app_id}/specification", status_code=status.HTTP_200_OK)
async def put_app_configuration_handler(
    kind: str,
    app_id: UUID,
    new_specification: dict[str, Any],
) -> AppOperationOK:
    """Update app specification and return OK response"""
    update_configuration(key="specification", new_data=new_specification)

    await send_message(
        topic="app_updates",
        key=str(app_id),
        value={"event": "specification updated", "kind": kind, "app_id": str(app_id)},
    )

    return AppOperationOK(kind=kind, app_id=app_id)


@router.put("/{kind}/{app_id}/settings", status_code=status.HTTP_200_OK)
async def put_app_settings_handler(
    kind: str,
    app_id: UUID,
    new_settings: dict[str, Any],
) -> AppOperationOK:
    """Update app settings and return OK response"""
    update_configuration(key="settings", new_data=new_settings)

    await send_message(
        topic="app_updates",
        key=str(app_id),
        value={"event": "settings updated", "kind": kind, "app_id": str(app_id)},
    )

    return AppOperationOK(kind=kind, app_id=app_id)


@router.put("/{kind}/{app_id}/state", status_code=status.HTTP_200_OK)
async def put_app_settings_handler(
    db_sessionmaker: Annotated[async_sessionmaker, Depends(get_db_sessionmaker)],
    kind: str,
    app_id: UUID,
    new_state: AppState,
) -> AppOperationOK:
    """Update app state and return OK response"""
    response = await update_app_state(
        db_sessionmaker=db_sessionmaker,
        kind=kind,
        app_id=app_id,
        new_state=new_state,
    )

    await send_message(
        topic="app_updates",
        key=str(app_id),
        value={"event": "state updated", "kind": kind, "app_id": str(app_id)},
    )

    return response


@router.delete("/{kind}/{app_id}", status_code=status.HTTP_200_OK)
async def put_app_settings_handler(
    db_sessionmaker: Annotated[async_sessionmaker, Depends(get_db_sessionmaker)],
    kind: str,
    app_id: UUID,
) -> AppOperationOK:
    """Delete app and return OK response"""
    response = await delete_app(
        db_sessionmaker=db_sessionmaker,
        kind=kind,
        app_id=app_id,
    )

    await send_message(
        topic="app_updates",
        key=str(app_id),
        value={"event": "app deleted", "kind": kind, "app_id": str(app_id)},
    )

    return response
