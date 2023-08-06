from __future__ import annotations

from typing import Type, TypeVar, Dict, List, Optional

from pyfactcast.grpc.generated.FactStore_pb2 import MSG_Notification
from pydantic import BaseModel, Extra, constr

import json

F = TypeVar("F", bound="Fact")


class CatchUp:
    pass


# Sadly pydantic and mypy do not play nice here.
Id: constr = constr(  # type: ignore
    regex=r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
)
AggsId: constr = constr(  # type: ignore
    regex=r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
)


class FactHeader(BaseModel):
    class Config:
        extra = Extra.allow

    ns: str
    type: str
    id: Id  # type: ignore
    aggIds: Optional[List[AggsId]] = None  # type: ignore
    meta: Dict[str, str] = {}


class Fact(BaseModel):
    header: FactHeader
    payload: Dict

    @classmethod
    def from_msg(cls: Type[F], msg: MSG_Notification) -> F:
        return cls(
            header=json.loads(msg.fact.header), payload=json.loads(msg.fact.payload)
        )


class VersionedType(BaseModel):
    type: str
    version: int = 0
