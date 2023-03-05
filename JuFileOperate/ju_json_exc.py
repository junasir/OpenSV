

from JuFileOperate.ju_json_operate import JuJsonOperate


file, _, result = JuJsonOperate.ju_load_json("2.json")
if _:
    nodes = file["nodes"]
    edges = file["edges"]
    print(file)

def _get_bottom(nodes, edges):
    for value in nodes:
        if value["outputs"]:
            pass

def search_info(edges, s_key, s_value):
    lis = []
    for key, value in edges:
        if s_key in value.keys():
            if s_value == value[s_key]:
                lis.append(value)
    return lis
