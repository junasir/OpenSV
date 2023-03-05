from copy import copy, deepcopy
# from queue import Queue
from threading import Thread
from time import sleep

from PySide2.QtCore import QObject, Signal


class run_module(QObject):
    s_return = Signal()

    def __init__(self, parent=None, queue=None, device=None, log=None):
        super().__init__()
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
                                    get_input = _class.getInputs()
                                    for j in range(input_len):
                                        input_node_default_parm = get_input[j].grNode.default_parm
                                        if input_node_default_parm["result_flag"]:
                                            if input_value[i] in input_node_default_parm["result"]:
                                                # value[i] = input_node_default_parm["result"][variable_list[i]]
                                                value.append(input_node_default_parm["result"][input_value[i]])
                                        else:
                                            pass
                                else:
                                    value.append(input_value[i])


                            # value = []
                            # variable_list = default_parm["variable_input"]
                            # for i in range(len(variable_list)):
                            #     get_input = _class.getInputs()
                            #     for j in range(input_len):
                            #         input_node_default_parm = get_input[j].grNode.default_parm
                            #         if input_node_default_parm["result_flag"]:
                            #             if variable_list[i] in input_node_default_parm["result"]:
                            #                 value.append(input_node_default_parm["result"][variable_list[i]])
                            #         else:
                            #             pass
                            value.append(_class.content)
                            result = getattr(func, default_parm.get("operation_func"))(*value)
                            if result[0]:
                                _class.markDirty(True)
                                _class.markInvalid(False)
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
                                    for j in range(input_len):
                                        input_node_default_parm = get_input[j].grNode.default_parm
                                        if input_node_default_parm["result_flag"]:
                                            if input_value[i] in input_node_default_parm["result"]:
                                                # value[i] = input_node_default_parm["result"][variable_list[i]]
                                                value.append(input_node_default_parm["result"][input_value[i]])
                                        else:
                                            pass
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
