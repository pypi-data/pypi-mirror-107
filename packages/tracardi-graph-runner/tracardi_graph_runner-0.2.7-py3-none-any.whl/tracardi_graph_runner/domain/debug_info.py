from typing import List

from pydantic import BaseModel

from tracardi_graph_runner.domain.debug_call_info import DebugCallInfo
from tracardi_graph_runner.domain.debug_node_info import DebugNodeInfo
from tracardi_graph_runner.domain.init_result import InitResult


class DebugInfo(BaseModel):
    init: InitResult
    run: List[DebugNodeInfo] = []
    calls: List[DebugCallInfo] = []
