from uuid import UUID

from sqlalchemy import and_, update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.controllers.app import get_app
from database.models import AppModel
from schemas.v1.app import AppOperationOK
from schemas.v1.errors import DBAPICallError
from schemas.v1.generated import Document


async def update_app_json(
    db_sessionmaker: async_sessionmaker,
    kind: str,
    app_id: UUID,
    new_json: Document,
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
            msg=f"can not save json to app with kind={kind} and app_id={app_id}"
        ) from e

    return AppOperationOK(kind=kind, app_id=app_id)
    