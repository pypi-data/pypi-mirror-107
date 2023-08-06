from uuid import UUID

import orjson
from pydantic import BaseModel, validator

from .helpers import orjson_dumps


class Model(BaseModel):
    @validator("id", check_fields=False)
    def id_must_be_uuid(cls, v):
        if isinstance(v, UUID):
            return str(v)
        else:
            return UUID(v) and v

    @classmethod
    def is_type_dict(cls, field):
        return cls.__fields__[field].type_ == dict

    @classmethod
    def from_record(cls, record):
        data = {
            k: (v if not v or not cls.is_type_dict(k) else orjson.loads(v))
            for k, v in record.items()
            if k in cls.__fields__
        }
        return cls(**data)

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        use_enum_values = True
