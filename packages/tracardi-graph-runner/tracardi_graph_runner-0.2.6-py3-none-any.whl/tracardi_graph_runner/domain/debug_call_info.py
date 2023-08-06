from typing import List, Optional

from pydantic import BaseModel

from tracardi_graph_runner.domain.entity import Entity
from tracardi_graph_runner.domain.input_params import InputParams
from tracardi_graph_runner.domain.action_result import ActionResult


class DebugCallInfo(BaseModel):
    node: Entity
    edge: Optional[Entity] = None
    input: Optional[InputParams] = None
    output: Optional[List[ActionResult]] = None
