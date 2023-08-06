from typing import List
from pydantic import BaseModel
from tracardi_graph_runner.domain.debug_call_info import DebugCallInfo


class DebugInfo(BaseModel):
    calls: List[DebugCallInfo] = []
