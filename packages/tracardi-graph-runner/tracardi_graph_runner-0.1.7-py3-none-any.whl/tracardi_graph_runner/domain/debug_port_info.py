from typing import Any, Optional

from pydantic import BaseModel

from tracardi_graph_runner.domain.input_params import InputParams
from tracardi_graph_runner.domain.task_result import TaskResult


class DebugPortInfo(BaseModel):
    output: Optional[TaskResult] = None
    input: Optional[InputParams] = None
    error: Optional[str] = None
