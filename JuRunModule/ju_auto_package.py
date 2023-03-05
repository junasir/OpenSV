from importlib import reload, import_module
from os import path, getcwd, walk, remove

CALC_NODES = {
}


class ConfException(Exception): pass


class InvalidNodeRegistration(ConfException): pass


class OpCodeNotRegistered(ConfException): pass


class Auto_Pack(object):
    def __init__(self, log=None):
        self.user_logger = log
        self.CALC_NODES = {}
        self.device = {}
        self.LISTBOX_MIMETYPE = "application/x-item"
        self.auto_get_ip_class_new()
        self.auto_get_device_class_new()
        # self.auto_get_ip_class()
        # self.auto_get_device_class()

    def register_node_now(self, op_code, class_reference):
        if op_code in self.CALC_NODES:
            raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" % (
                op_code, self.CALC_NODES[op_code]
            ))
        self.CALC_NODES[op_code] = class_reference

    def register_node(self, op_code, original_class):
        # def decorator(original_class):
        try:
            self.register_node_now(op_code, original_class)
        except BaseException as e:
            print(e)
            # return original_class

        # decorator(original_class)
        return original_class

    def get_class_from_opcode(self, op_code):
        if op_code not in self.CALC_NODES: raise OpCodeNotRegistered("OpCode '%s' is not registered" % op_code)
        return self.CALC_NODES[op_code]

    def auto_get_ip_class(self):
        self.CALC_NODES = {}
        list_1 = ["nodes1.Add", "nodes1.Div", "nodes1.Input", "nodes1.Mul", "nodes1.Output", "nodes1.Sub"]
        list_2 = ["CalcNode_Add", "CalcNode_Div", "CalcNode_Input", "CalcNode_Mul", "CalcNode_Output", "CalcNode_Sub"]
        for i in range(len(list_1)):
            ip_class_name = list_2[i]
            module = import_module(list_1[i])
            reload(module)

            #
            # register_node(OP_NODE_OUTPUT, module)
            # module = register_node(ip_class_name)
            ip_class_object = getattr(module, ip_class_name)
            self.CALC_NODES[ip_class_name] = ip_class_object

        print(self.CALC_NODES)

    def auto_get_device_class(self):
        self.device = {}
        list_1 = ["device.opencv.opencv_test.opencv_test"]
        list_2 = ["opencv"]
        list_3 = ["opencv_test"]
        # list_4 = ["opencv"]
        for i in range(len(list_1)):
            ip_class_name = list_3[i]
            module = import_module(list_1[i])
            reload(module)

            #
            # register_node(OP_NODE_OUTPUT, module)
            # module = register_node(ip_class_name)
            ip_class_object = getattr(module, ip_class_name)()
            temp = {ip_class_name: ip_class_object}
            self.device[list_2[i]] = temp

        print(self.device)
    # import all nodes and register them

    def auto_get_ip_class_new(self):
        self.CALC_NODES = {}
        self.CALC_NODES_TYPE = {}
        package_path = path.join(getcwd(), "JuPluginPack\\JuIp")
        try:
            for root_path, dirs, files in walk(package_path):
                if "_Pack" == root_path[-5:]:
                    class_type = root_path.split("\\")[-2]
                    print(root_path, dirs, files)
                    if "__pycache__" not in root_path:
                        for file in files:
                            if "_backup_" not in file:
                                name, _ = file.split(".")
                                if _ == "py" or _ == "pyc":
                                    dir_name_list = root_path[root_path.find("JuPluginPack\\JuIp"):].split("\\")
                                    file_new = dir_name_list[-1].replace("_Pack", "").title()
                                    module_path = ""
                                    for key in dir_name_list:
                                        module_path = module_path + key + "."
                                    module_path = module_path + name
                                    module = import_module(module_path)
                                    reload(module)
                                    ip_class = "JuIp" + file_new.replace("_", "")
                                    ip_class_object = getattr(module, ip_class)
                                    ip_class_name = ip_class_object.op_code
                                    self.CALC_NODES[ip_class_name] = ip_class_object
                                    if class_type not in self.CALC_NODES_TYPE:
                                        self.CALC_NODES_TYPE[class_type] = [ip_class_name]
                                    else:
                                        self.CALC_NODES_TYPE[class_type].append(ip_class_name)
                            else:
                                self._del_file(root_path + "/" + file)
        except BaseException as e:
            self.user_logger.info(e)
        print(self.CALC_NODES)

    def auto_get_device_class_new(self):
        self.device = {}
        package_path = path.join(getcwd(), "JuPluginPack\\JuDevice")
        try:
            for root_path, dirs, files in walk(package_path):
                if "_Pack" in root_path:
                    print(root_path, dirs, files)
                    for file in files:
                        try:
                            if "cpython" not in file:
                                name, _ = file.split(".")
                                if _ == "py" or _ == "pyc":
                                    dir_name_list = root_path[root_path.find("JuPluginPack\\JuDevice"):].split("\\")
                                    path_folder = dir_name_list[-2]
                                    file_new = dir_name_list[-1].replace("_Pack", "").title()
                                    module_path = ""
                                    for key in dir_name_list:
                                        module_path = module_path + key + "."
                                    module_path = module_path + name
                                    module = import_module(module_path)
                                    reload(module)
                                    ip_class = "Ju" + file_new.replace("_", "")
                                    # ip_class_object = getattr(module, ip_class)()
                                    ip_class_object = getattr(module, ip_class)(self.user_logger)
                                    if path_folder in self.device.keys():
                                        self.device[path_folder][ip_class] = ip_class_object
                                    else:
                                        temp = {ip_class: ip_class_object}
                                        self.device[path_folder] = temp
                                    # ip_class_name = ip_class_object.op_code
                                    # self.CALC_NODES[ip_class_name] = ip_class_object
                        except BaseException as e:
                            print(e)
        except BaseException as e:
            self.user_logger.info(e)
        print(self.device)

    def show_device(self):
        init_device = {}
        for keys in self.device.keys():
            lis = [{"name": keys, "vendor_name": keys}]
            init_device[keys] = lis
        # init_device = {"opencv": [{"name": "opencv", "vendor_name": "opencv"}]}
        return init_device

    def ip_device_reconnect(self):
        self.auto_get_ip_class_new()
        self.auto_get_device_class_new()

    def _del_file(self, file_path):
        try:
            if path.exists(file_path):
                remove(file_path)
        except Exception:
            pass

#
# if __name__ == "__main__":
#     auto_pack = Auto_Pack()
