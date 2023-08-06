from typing import List

from pydantic import BaseModel

from tracardi_graph_runner.domain.debug_node_info import DebugNodeInfo


class DebugInfo(BaseModel):
    info: List[DebugNodeInfo] = []
