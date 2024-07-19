from sqlalchemy.orm import as_declarative


@as_declarative()
class BaseModel:
    def as_dict(self, exclude: list[str] | None = None) -> dict:
        res_dict = {}

        for column in self.__table__.columns:
            if not exclude or column.name not in exclude:
                res_dict[column.name] = (
                    str(getattr(self, column.name)) if getattr(self, column.name) else None
                )

        return res_dict
