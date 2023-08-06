from typing import List, Optional

from pydantic import BaseModel
from tracardi_plugin_sdk.domain.register import Plugin


# class Spec(BaseModel):
#     className: str
#     module: str
#     inputs: Optional[List[str]] = []
#     outputs: Optional[List[str]] = []
#     init: Optional[dict] = {}


class Position(BaseModel):
    x: int
    y: int


# class MetaData(BaseModel):
#     name: str
#     desc: Optional[str] = ""
#     type: str
#     width: int
#     height: int
#     icon: str


class SimplifiedSpec(BaseModel):
    module: str


class Node(BaseModel):
    id: str
    type: str
    position: Position
    data: Plugin


class Edge(BaseModel):
    source: str
    sourceHandle: str
    target: str
    targetHandle: str
    id: str
    type: str


class FlowGraphData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
