import asyncio

from database.connection import get_db_sessionmaker
from database.controllers.app import create_app
from settings import yaml_data


async def main():
    print("Создание приложения...")
    db_sessionmaker = get_db_sessionmaker()
    await create_app(
        db_sessionmaker=db_sessionmaker,
        kind=yaml_data["kind"],
        name=yaml_data["name"],
        version=yaml_data["version"],
        description=yaml_data["description"],
    )
    print("Приложение успешно создано!")


if __name__ == "__main__":
    asyncio.run(main())
