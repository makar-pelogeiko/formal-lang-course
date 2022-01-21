from project.interpreter_gql.memory import MemBox
from pyformlang.regular_expression import Regex
from pyformlang.regular_expression.regex_objects import Symbol
from project.interpreter_gql.interpreter_utils.type_utils import get_target_type
from pyformlang.finite_automaton import State
from project.interpreter_gql.interpreter_utils.interpreter_except import InterpError


def set_or_add_start_states(source: MemBox, states: MemBox, reset: bool):
    name = "add_start_states fun"
    if reset:
        name = "set_start_states fun"

    allow_types = ["dfa", "regex", "str"]
    if not isinstance(source, MemBox) or not isinstance(states, MemBox):
        raise InterpError([f"{name}"], f"Params in not correct internal type")

    if source.v_type not in allow_types or source.is_list:
        raise InterpError([f"{name}"], f"Source is not in allowed types")

    if not states.is_list:
        raise InterpError([f"{name}"], f"Iterable states required")

    mem_dfa = get_target_type(source, "dfa")

    if reset:
        temp_set = mem_dfa.value.start_states
        for st in temp_set:
            mem_dfa.value.remove_start_state(st)

    try:
        for st in states.value:
            mem_dfa.value.add_start_state(State(st))
    except:
        raise InterpError([f"{name}"], f"Exception in adding start states")

    return mem_dfa


def set_or_add_final_states(source: MemBox, states: MemBox, reset: bool):
    name = "add_final_states fun"
    if reset:
        name = "set_final_states fun"

    allow_types = ["dfa", "regex", "str"]
    if not isinstance(source, MemBox) or not isinstance(states, MemBox):
        raise InterpError([f"{name}"], f"Params in not correct internal type")

    if source.v_type not in allow_types or source.is_list:
        raise InterpError([f"{name}"], f"Source is not in allowed types")

    if not states.is_list:
        raise InterpError([f"{name}"], f"Iterable states required")

    mem_dfa = get_target_type(source, "dfa")

    if reset:
        temp_set = mem_dfa.value.final_states
        for st in temp_set:
            mem_dfa.value.remove_final_state(st)

    try:
        for st in states.value:
            mem_dfa.value.add_final_state(State(st))
    except:
        raise InterpError([f"{name}"], f"Exception in adding final states")

    return mem_dfa
