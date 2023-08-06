from typing import List, Optional

from pydantic import BaseModel

from tracardi_graph_runner.domain.debug_port_info import DebugPortInfo


class DebugNodeInfo(BaseModel):
    node: str
    init: Optional[dict] = None
    ports: List[DebugPortInfo] = []
