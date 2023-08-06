from typing import List, Optional
from pydantic import BaseModel


class Spec(BaseModel):
    className: str
    module: str
    inputs: Optional[List[str]] = []
    outputs: Optional[List[str]] = []
    init: Optional[dict] = {}


class MetaData(BaseModel):
    name: str
    desc: Optional[str] = ""
    type: str
    width: int
    height: int
    icon: str


class Plugin(BaseModel):
    start: bool = False
    spec: Spec
    metadata: MetaData
