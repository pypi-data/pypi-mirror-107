import asyncio
import importlib
from pprint import pprint
from typing import List

from pydantic import BaseModel
from tracardi_plugin_sdk.action_runner import ActionRunner

from .debug_call_info import DebugCallInfo
from .debug_info import DebugInfo
from .debug_node_info import DebugNodeInfo
from .debug_port_info import DebugPortInfo
from .entity import Entity
from .init_result import InitResult
from .input_params import InputParams
from .action_result import ActionResult
from ..utils.dag_error import DagError, DagExecError
from .edge import Edge
from .node import Node
from .tasks_results import ActionsResults


class ExecutionGraph(BaseModel):
    graph: List[Node]
    start_nodes: list

    @staticmethod
    def _add_to_event_loop(tasks, coroutine, port, params, edge_id) -> list:
        task = asyncio.create_task(coroutine)
        tasks.append((task, port, params, edge_id))
        return tasks

    async def _void_return(self, node):
        all_outputs = [ActionResult(port=_start_port, value=None)
                       for _start_port in node.graph.out_edges.get_start_ports()]
        if len(all_outputs) == 1:
            return all_outputs[0]
        else:
            return tuple(all_outputs)

    @staticmethod
    def _null_params(node):
        pass

    def _run_in_event_loop(self, tasks, node, params, _port, _task_result, edge_id):
        exec_result = node.object.run(**params)
        return self._add_to_event_loop(tasks, exec_result, port=_port, params=_task_result, edge_id=edge_id)

    async def run_task(self, node: Node, payload, ready_actions_results: ActionsResults):

        if isinstance(node.object, DagExecError):
            raise node.object

        tasks = []

        if node.graph.in_edges:

            # Prepare value

            for start_port, edge, end_port in node.graph.in_edges:  # type: str, Edge, str

                for action_result in ready_actions_results.get(edge.id, start_port):  # type: ActionResult

                    result_copy = action_result.copy(deep=True)

                    # Do not trigger fun for None values

                    params = {end_port: result_copy.value}
                    if result_copy.value is not None:

                        # Run spec with every downstream message (param)
                        # Runs as many times as downstream edges

                        tasks = self._run_in_event_loop(tasks, node, params, end_port, action_result.value, edge.id)

                    else:

                        # If downstream spec returns None. Return None for all its upstream edges
                        exec_result = self._void_return(node)
                        tasks = self._add_to_event_loop(tasks, exec_result, end_port, action_result.value, edge.id)

        else:

            # This is first node in graph

            if node.start:
                _port = "payload"
                _payload = payload
            else:
                _port = None
                _payload = None

            params = {"payload": payload}
            tasks = self._run_in_event_loop(tasks, node, params, _port, _payload, None)

        # Yield tasks results
        for task, port, params, edge_id in tasks:
            try:
                result = await task
            except BaseException as e:
                msg = "The following error occurred `{}` when running node `{}`. ". \
                          format(str(e), node.id) + "Check run method of `{}.{}`". \
                          format(node.module, node.className)
                raise DagExecError(msg,
                                   port=port,
                                   input=params)

            yield result, port, params, edge_id

    @staticmethod
    def _add_results(task_results: ActionsResults, node: Node, result: ActionResult) -> ActionsResults:
        for _, edge, _ in node.graph.out_edges:
            result_copy = result.copy(deep=True)
            task_results.add(edge.id, result_copy)
        return task_results

    @staticmethod
    def _get_object(node: Node, params=None) -> ActionRunner:
        module = importlib.import_module(node.module)
        task_class = getattr(module, node.className)
        if params:
            return task_class(**params)
        return task_class()

    def init(self) -> InitResult:
        errors = []
        objects = []
        for node in self.graph:
            # Init object
            try:
                node.object = self._get_object(node, node.init)
                objects.append("{}.{}".format(node.module, node.className))
            except Exception as e:
                msg = "The following error occurred `{}` when initializing node `{}`. ".format(
                    str(e), node.id) + "Check __init__ of `{}.{}`".format(node.module, node.className)

                errors.append(msg)
                node.object = DagExecError(msg,
                                           port=None,
                                           input=None)

        return InitResult(errors=errors, objects=objects)

    @staticmethod
    def _is_result(result):
        return hasattr(result, 'port') and hasattr(result, 'value')

    @staticmethod
    def _get_debug_info(port, input_params, result):
        if port is None and input_params is None:
            input = None
        else:
            input = InputParams(port=port, value=input_params)

        return DebugPortInfo(input=input, output=result)

    def _post_process_result(self, port, input_params, tasks_results, result, node, debug_node_info) -> ActionsResults:
        if result is not None:
            tasks_results = self._add_results(tasks_results, node, result)
        else:
            # Check if there are any ports bu no output
            if len(node.outputs) > 0:
                raise DagError(
                    "Action (Node: {}) did not return Result object though there are the following output ports open {}".format(
                        node.id, node.outputs),
                    port=port,
                    input=input_params
                )

        info = self._get_debug_info(port, input_params, result)
        debug_node_info.ports.append(info)

        return tasks_results

    async def run(self, init: InitResult, payload) -> DebugInfo:

        actions_results = ActionsResults()
        debug_info = DebugInfo(init=init)

        for node in self.graph:  # type: Node

            debug_node_info = DebugNodeInfo(node=node.id, init=node.init)

            try:

                async for result, input_port, input_params, in_edge_id in \
                        self.run_task(node, payload, ready_actions_results=actions_results):

                    # Save call debug info

                    if self._is_result(result):
                        result_output = [result]
                    else:
                        result_output = result

                    call_debug_info = DebugCallInfo(
                        node=Entity(id=node.id),
                        edge=Entity(id=in_edge_id) if in_edge_id is not None else None,
                        input=InputParams(port=input_port, value=input_params),
                        output=result_output
                    )

                    debug_info.calls.append(call_debug_info)

                    # Process result

                    if isinstance(result, tuple):
                        for sub_result in result:  # type: ActionResult
                            if self._is_result(sub_result) or sub_result is None:
                                actions_results = self._post_process_result(
                                    input_port,
                                    input_params,
                                    actions_results,
                                    sub_result,
                                    node,
                                    debug_node_info)
                            else:
                                raise DagError(
                                    "Action (Node: {}) did not return Result or tuple of Results. Expected Result got {}".format(
                                        node.id, type(result)),
                                    port=input_port,
                                    input=input_params
                                )

                    elif self._is_result(result) or result is None:
                        actions_results = self._post_process_result(
                            input_port,
                            input_params,
                            actions_results,
                            result,
                            node,
                            debug_node_info)
                    else:
                        raise DagError(
                            "Action (Node: {}) did not return Result or tuple of Results. Expected Result got {}".format(
                                node.id, type(result)),
                            port=input_port,
                            input=input_params)

            except (DagError, DagExecError) as e:

                if e.input is not None and e.port is not None:
                    e = DebugPortInfo(
                        error=str(e),
                        input=InputParams(port=e.port, value=e.input)
                    )
                else:
                    e = DebugPortInfo(
                        error=str(e)
                    )

                debug_node_info.ports.append(e)

            debug_info.run.append(debug_node_info)

        return debug_info

    def serialize(self):
        return self.dict()
