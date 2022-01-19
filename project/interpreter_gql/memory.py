from project.interpreter_gql.interpreter_utils.interpreter_except import InterpError


class MemoryList:
    def __init__(self):
        self.run_memory = dict()
        self.stack = dict()

    def is_exist_stack(self, key):
        if key in self.stack.keys():
            return True
        else:
            return False

    def del_elem_stack(self, key):
        if self.is_exist_stack(key):
            del self.stack[key]

    def set_elem_stack(self, key, elem):
        self.stack[key] = elem

    def set_elem(self, key, elem):
        self.run_memory[key] = elem

    def get_elem(self, key):
        if self.is_exist_stack(key):
            return self.stack[key]

        if key in self.run_memory.keys():
            return self.run_memory[key]
        else:
            raise InterpError(["memory call"], f"No value with name: {key}")

    def get_addr_elem(self, key, addr_list):
        if key in self.run_memory.keys():
            box = self.run_memory[key]
            box = MemBox()
            if not box.is_list:
                raise InterpError(
                    ["memory call"], f"Value in memory is not iterable: {key}"
                )
            try:
                temp_val = box.value[addr_list[0]]
                temp_lst = addr_list[1:]
                for i in temp_lst:
                    temp_val = temp_val[i]
            except:
                raise InterpError(
                    ["memory call"], f"Error in iterate memory value: {key}"
                )

            return temp_val

        else:
            raise InterpError(["memory call"], f"No value with name: {key}")


class MemBox:
    def __init__(self):
        self.is_list = False
        self.v_type = "def_type"
        # or self.value = list[v_type]
        self.value = 0

    def __init__(self, is_list, v_type, value):
        self.is_list = is_list
        self.v_type = v_type
        self.value = value

    def __str__(self):
        if self.v_type == "dfa":
            temp = self.value.to_regex()
            return str(temp)
        return str(self.value)
