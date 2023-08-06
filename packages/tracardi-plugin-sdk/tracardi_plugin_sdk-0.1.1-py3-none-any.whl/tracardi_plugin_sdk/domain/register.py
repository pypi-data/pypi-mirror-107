from typing import List, Optional
from pydantic import BaseModel


class Spec(BaseModel):
    className: str
    module: str
    inputs: List[str]
    outputs: List[str]
    init: Optional[dict] = {}


class MetaData(BaseModel):
    name: str
    desc: Optional[str] = ""
    type: str
    width: int
    height: int
    icon: str


class Plugin(BaseModel):
    spec: Spec
    metadata: MetaData
