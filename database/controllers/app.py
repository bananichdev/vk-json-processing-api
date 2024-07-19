from uuid import UUID

from sqlalchemy import and_, delete, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.models import AppModel
from schemas.v1.app import App, AppOperationOK, AppState
from schemas.v1.errors import AppNotFoundError, DBAPICallError


async def get_app(
    db_sessionmaker: async_sessionmaker,
    kind: str,
    app_id: UUID,
) -> App:
    try:
        async with db_sessionmaker.begin() as session:
            if (
                app_entity := await session.scalar(
                    select(AppModel).where(and_(AppModel.kind == kind, AppModel.app_id == app_id))
                )
            ) is None:
                raise AppNotFoundError(kind=kind, app_id=app_id)
    except DBAPIError as e:
        raise DBAPICallError(msg=f"can not get app with kind={kind} and app_id={app_id}") from e

    return App(**app_entity.as_dict())


async def create_app(
    db_sessionmaker: async_sessionmaker,
    kind: str,
    name: str,
    version: str,
    description: str,
) -> App:
    try:
        async with db_sessionmaker.begin() as session:
            app_entity = AppModel(
                kind=kind,
                name=name,
                version=version,
                description=description,
            )
            session.add(app_entity)
    except IntegrityError as e:
        raise ValueError(f"App with kind={kind} already exists") from e
    except DBAPIError as e:
        raise IOError(f"Can not create app") from e

    return App(**app_entity.as_dict())


async def update_app_state(
    db_sessionmaker: async_sessionmaker,
    kind: str,
    app_id: UUID,
    new_state: AppState,
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
                .values(state=new_state.state)
            )
    except DBAPIError as e:
        raise DBAPICallError(msg=f"can not update app with kind={kind} and app_id={app_id}") from e

    return AppOperationOK(kind=kind, app_id=app_id)


async def delete_app(
    db_sessionmaker: async_sessionmaker,
    kind: str,
    app_id: UUID,
) -> AppOperationOK:
    await get_app(
        db_sessionmaker=db_sessionmaker,
        kind=kind,
        app_id=app_id,
    )

    try:
        async with db_sessionmaker.begin() as session:
            await session.execute(
                delete(AppModel).where(and_(AppModel.kind == kind, AppModel.app_id == app_id))
            )
    except DBAPIError as e:
        raise DBAPICallError(msg=f"can not delete app with kind={kind} and app_id={app_id}") from e

    return AppOperationOK(kind=kind, app_id=app_id)
