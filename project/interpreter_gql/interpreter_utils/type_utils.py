from pyformlang.regular_expression import Regex
from project.interpreter_gql.memory import MemBox
from project.interpreter_gql.interpreter_utils.interpreter_except import InterpError


def states_type_checker(source, act):
    exc = None
    flag = True

    if not isinstance(source, MemBox):
        flag = False
        exc = InterpError([f"expr {act}"], "Not correct internal type")
    if source.v_type != "dfa":
        flag = False
        exc = InterpError([f"expr {act}"], "Automaton required to get states")

    return flag, exc


def check_int(s):
    if isinstance(s, int):
        return True
    elif isinstance(s, str):
        if s[0] in ("-", "+"):
            return s[1:].isdigit()
        return s.isdigit()
    else:
        return False


def get_target_type(obj: MemBox, target_type: str):
    if obj.v_type == "str":
        if target_type == "regex" or target_type == "dfa":
            obj.v_type = "regex"
            obj.value = Regex(obj.value)

    if obj.v_type == "regex":
        if target_type == "dfa":
            obj.v_type = "dfa"
            obj.value = obj.value.to_epsilon_nfa().to_deterministic()

    return obj
