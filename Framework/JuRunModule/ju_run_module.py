from copy import copy, deepcopy
# from queue import Queue
from threading import Thread
from time import sleep

from PySide2.QtCore import QObject, Signal


class run_module(QObject):
    s_return = Signal()

    def __init__(self, parent=None, queue=None, device=None, log=None, s_img=None):
        super().__init__()
        self.s_img = s_img
        self.user_logger = log
        self.queue = queue
        self.device = device
        _get_queue = Thread(target=self._get_queue)
        _get_queue.setDaemon(True)
        _get_queue.start()

    def _get_queue(self):
        while 1:
            if self.queue is not None:
                try:
                    msg = self.queue.get()
                    if isinstance(msg, dict):
                        if msg["mode"] == 1:
                            default_parm = deepcopy(msg["default_parm"])
                            func = self.device[default_parm["object"]["type"]][default_parm["operation_file"]]
                            _class = msg["_class"]
                            input_len = len(_class.inputs)
                            output_len = len(_class.outputs)
                            # get_input = []
                            # get_output = []
                            value = default_parm["value"]
                            result_dic = default_parm["result"]
                            if input_len == 0 and output_len > 0:
                                # result_flag = default_parm["result_flag"]
                                try:
                                    result = getattr(func, default_parm.get("operation_func"))(*value)
                                    if result[0]:
                                        output_result_key_list = default_parm["variable_output"]
                                        for i in range(len(output_result_key_list)):
                                            result_dic[output_result_key_list[i]] = result[1][i]
                                        default_parm["result_flag"] = True
                                        default_parm["result"] = result_dic
                                        _class.grNode.default_parm = default_parm
                                        _class.markDirty(True)
                                        _class.markInvalid(False)
                                except BaseException as e:
                                    _class.markDirty(False)
                                    _class.markInvalid(True)
                                    self.user_logger.error(e)
                                # else:
                                #     self.user_logger.error("=====")
                            elif input_len > 0 and output_len == 0:
                                try:
                                    value = []
                                    input_value = default_parm["value"]
                                    variable_list = default_parm["variable_input"]
                                    for i in range(len(input_value)):
                                        if input_value[i] in variable_list:
                                            _, info = self.get_node_info(_class.inputs, input_value[i], result=[])
                                            if _:
                                                value.append(info)
                                            else:
                                                self.user_logger.error("variable_input error")
                                                return
                                        else:
                                            value.append(input_value[i])
                                    value.append(_class.content)
                                    result = getattr(func, default_parm.get("operation_func"))(*value)
                                    if result[0]:
                                        _class.markDirty(True)
                                        _class.markInvalid(False)
                                        if result[2]:
                                            self.s_img.emit([result[1]])
                                    else:
                                        _class.markDirty(False)
                                        _class.markInvalid(True)
                                        self.user_logger.error(result[1])
                                except BaseException as e:
                                    _class.markDirty(False)
                                    _class.markInvalid(True)
                                    self.user_logger.error(e)
                            else:
                                try:
                                    value = []
                                    input_value = default_parm["value"]
                                    variable_list = default_parm["variable_input"]
                                    get_input = []
                                    for i in range(input_len):
                                        get_input.append(_class.getInput(i))
                                    for i in range(len(input_value)):
                                        if input_value[i] in variable_list:
                                            _, info = self.get_node_info(_class.inputs, input_value[i], result=[])
                                            value.append(info)
                                        else:
                                            value.append(input_value[i])
                                    # value.append(_class.content)
                                    result = getattr(func, default_parm.get("operation_func"))(*value)
                                    if result[0]:
                                        output_result_key_list = default_parm["variable_output"]
                                        for i in range(len(output_result_key_list)):
                                            result_dic[output_result_key_list[i]] = result[1][i]
                                        default_parm["result_flag"] = True
                                        default_parm["result"] = result_dic
                                        _class.grNode.default_parm = default_parm
                                        _class.markDirty(True)
                                        _class.markInvalid(False)
                                    else:
                                        self.user_logger.error(result[1])
                                except BaseException as e:
                                    _class.markDirty(False)
                                    _class.markInvalid(True)
                                    self.user_logger.error(e)
                        elif msg["mode"] == 2:
                            lis_ = []
                            current_node = msg["_class"]
                            self.get_all_node(current_node, lis_)
                            pass
                except BaseException as e:
                    self.user_logger.error(e)
                # parm = copy(default_parm)
                # parm["content"] = _class.content
                # func = self.device[parm["object"]["type"]][parm["operation_file"]]
                # try:
                #     parm_ = getattr(func, parm.get("operation_func"))(parm)
                #     _class.grNode.default_parm = parm_
                # except BaseException as e:
                #     print(e)
            sleep(0.1)

    def get_all_node(self, node_class, lis_all):

        pass

    def get_node_info(self, input=None, value=None, result=None):
        for l in input:
            node = l.edges
            for i in node:
                if "start_socket" in i.__dir__():
                    default_parm_node = i.start_socket.node
                    default_parm = default_parm_node.grNode.default_parm
                    for k in range(len(default_parm["variable_output"])):
                        if value == default_parm["variable_output"][k]:
                            result.append(True)
                            result.append(default_parm["result"][value])
                            break
                        # self.combox_list.append(default_parm["variable_output"][k])
                    self.get_node_info(default_parm_node.inputs, value=value, result=result)
                if len(result) > 0:
                    break
            if len(result) > 0:
                break
        if len(result) == 0:
            result = [False, None]
        return result
