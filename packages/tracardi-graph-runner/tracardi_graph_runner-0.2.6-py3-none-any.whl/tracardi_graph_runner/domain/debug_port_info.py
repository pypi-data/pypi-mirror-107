from typing import Any, Optional

from pydantic import BaseModel

from tracardi_graph_runner.domain.input_params import InputParams
from tracardi_graph_runner.domain.action_result import ActionResult


class DebugPortInfo(BaseModel):
    output: Optional[ActionResult] = None
    input: Optional[InputParams] = None
    error: Optional[str] = None
