import asyncio
import importlib
from typing import List
from pydantic import BaseModel
from tracardi_plugin_sdk.action_runner import ActionRunner

from .debug_info import DebugInfo
from .debug_node_info import DebugNodeInfo
from .debug_port_info import DebugPortInfo
from .init_result import InitResult
from .input_params import InputParams
from .task_result import TaskResult
from ..utils.dag_error import DagError
from .edge import Edge
from .node import Node
from .tasks_results import TasksResults


class ExecutionGraph(BaseModel):
    graph: List[Node]
    start_nodes: list

    @staticmethod
    def _add_to_event_loop(tasks, coroutine, port, params) -> list:
        task = asyncio.create_task(coroutine)
        tasks.append((task, port, params))
        return tasks

    async def _void_return(self, node):
        all_outputs = [TaskResult(port=_start_port, value=None)
                       for _start_port in node.graph.out_edges.get_start_ports()]
        if len(all_outputs) == 1:
            return all_outputs[0]
        else:
            return tuple(all_outputs)

    @staticmethod
    def _null_params(node):
        pass

    async def run_task(self, node: Node, payload, ready_task_results: TasksResults):

        if node.object is None:
            raise DagError("Task (Node: {}) did not init properly. Is module {} and class {} present?".format(
                node.id, node.module, node.className), port=None)

        tasks = []

        if node.graph.in_edges:

            # Prepare value

            for start_port, edge, end_port in node.graph.in_edges:  # type: str, Edge, str

                for task_result in ready_task_results.get(edge.id, start_port):  # type: TaskResult

                    result_copy = task_result.copy(deep=True)

                    # Do not trigger fun for None values

                    params = {end_port: result_copy.value}
                    if result_copy.value is not None:

                        # Run spec with every downstream message (param)
                        # Runs as many times as downstream edges

                        exec_result = node.object.run(**params)
                        tasks = self._add_to_event_loop(tasks, exec_result, end_port, task_result.value)

                    else:

                        # If downstream spec returns None. Return None for all its upstream edges
                        exec_result = self._void_return(node)
                        tasks = self._add_to_event_loop(tasks, exec_result, end_port, task_result.value)

        else:

            # This is first node in graph

            if node.start:
                tasks = self._add_to_event_loop(tasks, node.object.run(payload=payload), port='payload', params=payload)
            else:
                tasks = self._add_to_event_loop(tasks, node.object.run(payload=payload), port=None, params=None)

        # Yield tasks results
        for task, port, params in tasks:
            result = await task
            yield result, port, params

    @staticmethod
    def _add_results(task_results: TasksResults, node: Node, result: TaskResult) -> TasksResults:
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
                errors.append(str(e))

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

    def _post_process_result(self, port, input_params, tasks_results, result, node, debug_node_info) -> TasksResults:
        if result is not None:
            tasks_results = self._add_results(tasks_results, node, result)
        else:
            # Check if there are any ports bu no output
            if len(node.outputs) > 0:
                raise DagError(
                    "Task (Node: {}) did not return Result object though there are the following output ports open {}".format(
                        node.id, node.outputs), port=port
                )

        info = self._get_debug_info(port, input_params, result)
        debug_node_info.ports.append(info)

        return tasks_results

    async def run(self, init: InitResult, payload) -> DebugInfo:

        tasks_results = TasksResults()
        debug_info = DebugInfo(init=init)

        for node in self.graph:  # type: Node

            debug_node_info = DebugNodeInfo(node=node.id, init=node.init)
            try:

                async for result, port, input_params in self.run_task(node, payload, ready_task_results=tasks_results):

                    if isinstance(result, tuple):
                        for sub_result in result:  # type: TaskResult
                            if self._is_result(sub_result) or sub_result is None:
                                tasks_results = self._post_process_result(
                                    port,
                                    input_params,
                                    tasks_results,
                                    sub_result,
                                    node,
                                    debug_node_info)

                                # if sub_result is not None:
                                #     tasks_results = self._add_results(tasks_results, node, sub_result)
                                #
                                # info = self._get_debug_info(port, input_params, sub_result)
                                # debug_node_info.ports.append(info)
                            else:
                                raise DagError(
                                    "Task (Node: {}) did not return Result or tuple of Results. Expected Result got {}".format(
                                        node.id, type(result)), port=port
                                )

                    elif self._is_result(result) or result is None:
                        tasks_results = self._post_process_result(
                            port,
                            input_params,
                            tasks_results,
                            result,
                            node,
                            debug_node_info)

                        # if result is not None:
                        #     tasks_results = self._add_results(tasks_results, node, result)
                        #
                        # info = self._get_debug_info(port, input_params, result)
                        # debug_node_info.ports.append(info)
                    else:
                        raise DagError(
                            "Task (Node: {}) did not return Result or tuple of Results. Expected Result got {}".format(
                                node.id, type(result)), port=port)
            except DagError as e:

                e = DebugPortInfo(
                    error=str(e)
                )

                debug_node_info.ports.append(e)

            debug_info.run.append(debug_node_info)

        return debug_info

    def serialize(self):
        return self.dict()
