from copy import copy, deepcopy
# from queue import Queue
from threading import Thread
from time import sleep, time

from PySide2.QtCore import QObject, Signal


class run_module(QObject):
    s_return = Signal()

    def __init__(self, parent=None, queue=None, device=None, log=None, s_img=None):
        super().__init__()
        self.s_img = s_img
        self.user_logger = log
        self.queue = queue
        self.device = device
        self._stop_flag = False
        self.thread_mode_2 = None
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
                                    a = time()
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
                                    # b = time()
                                    # self.user_logger.info(str(b - a))
                                except BaseException as e:
                                    _class.markDirty(False)
                                    _class.markInvalid(True)
                                    self.user_logger.error(e)
                            else:
                                try:
                                    # a = time()
                                    value = []
                                    input_value = default_parm["value"]
                                    variable_list = default_parm["variable_input"]
                                    get_input = []
                                    for i in range(input_len):
                                        get_input.append(_class.getInput(i))
                                    for i in range(len(input_value)):
                                        if input_value[i] in variable_list:

                                            _, info = self.get_node_info(_class.inputs, input_value[i], result=[])

                                            # self.user_logger.info(str(b - a))
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
                                        _class.grNode.default_parm = deepcopy(default_parm)
                                        _class.markDirty(True)
                                        _class.markInvalid(False)
                                    else:
                                        self.user_logger.error(result[1])
                                    if result[2]:
                                        self.s_img.emit([result[1]])
                                    # b = time()
                                    # self.user_logger.info(str(b - a))
                                except BaseException as e:
                                    _class.markDirty(False)
                                    _class.markInvalid(True)
                                    self.user_logger.error(e)
                                    if self.thread_mode_2 is not None:
                                        if self.thread_mode_2.is_alive():
                                            self._stop_flag = True
                        elif msg["mode"] == 2:
                            if msg["flag"] == "start":
                                current_node = msg["_class"]
                                node = self.get_top_node(current_node.inputs)
                                self._stop_flag = False
                                self.thread_mode_2 = Thread(target=self.start_node, args=(node,))
                                self.thread_mode_2.start()
                                print(node)
                            elif msg["flag"] == "stop":
                                if self._stop_flag is False:
                                    self._stop_flag = True
                            pass
                        elif msg["mode"] == 3:
                            func = msg["func"]
                            func.cap.release()
                except BaseException as e:
                    self.user_logger.error(e)
            sleep(0.0001)

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

    def get_top_node(self, input):
        for l in input:
            node = l.edges
            if node == []:
                info = l.node
            else:
                for i in node:
                    default_parm_node = i.start_socket.node
                    if "start_socket" in i.__dir__():
                        # default_parm = default_parm_node.grNode.default_parm
                        # for k in range(len(default_parm["variable_output"])):
                        #     self.combox_list.append(default_parm["variable_output"][k])
                        if default_parm_node.inputs == []:
                            return default_parm_node
                        else:
                            info = self.get_top_node(default_parm_node.inputs)
        return info

    def start_node(self, node):
        self.run_list = []
        self.while_run_list = []
        while 1:
            try:
                a = time()
                if self._stop_flag:
                    self._stop_flag = False
                    if self.while_run_list[0]["_class"].grNode.default_parm["value"][1] == "video":
                        default_parm = self.while_run_list[0]["_class"].grNode.default_parm
                        self.queue.put({"mode": 3, "func": self.device[default_parm["object"]["type"]]
                        [default_parm["operation_file"]]})
                    break
                try:
                    if len(self.while_run_list) > 0:
                        for i in self.while_run_list:
                            if self._stop_flag:
                                break
                            # c = time()
                            self.queue.put(i)
                            # d = time()
                            # print("---------", d - c)
                    else:
                        info = {"_class": node, "default_parm": node.grNode.default_parm, "mode": 1}
                        self.run_list.append(info)
                        self.queue.put(info)
                        self._start_node(node)
                        for i in range(len(self.run_list)):
                            temp = self.run_list[i]["_class"]
                            if temp.op_code == "CalcNode_Input":
                                if temp.grNode.default_parm["value"][1] == "video":
                                    for j in range(i, len(self.run_list)):
                                        self.while_run_list.append(self.run_list[j])
                                    break
                except BaseException as e:
                    self.user_logger.error(e)
                b = time()
                print("==================", b - a)
                sleep(0.001)
            except BaseException as e:
                self.user_logger.error(e)

    def _start_node(self, node):
        if self._stop_flag:
            return
        if len(node.outputs) > 0:
            if len(node.outputs[0].edges) > 0:
                temp_node = node.outputs[0].edges[0].end_socket.node
                info = {"_class": temp_node, "default_parm": temp_node.grNode.default_parm, "mode": 1}
                self.run_list.append(info)
                self.queue.put(info)
                self._start_node(temp_node)
