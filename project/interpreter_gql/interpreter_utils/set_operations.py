from pyformlang.regular_expression import Regex
from pyformlang.regular_expression.regex_objects import Symbol
from project.interpreter_gql.memory import MemBox
from project.interpreter_gql.interpreter_utils.type_utils import get_target_type
from project.interpreter_gql.interpreter_utils.interpreter_except import InterpError


def kleene_star(arg):
    allow_types = ["dfa", "regex", "str"]
    worked = arg

    if type(arg) == str:
        worked = MemBox(False, "str", arg)

    if type(worked) != MemBox:
        raise InterpError(["kleene func"], "Arg is not in correct internal type")
    if worked.v_type not in allow_types or worked.is_list:
        raise InterpError(["kleene func"], "Arg is not in allowed type for operation")

    if worked.v_type == "dfa":
        result = MemBox(
            False, "dfa", worked.value.kleene_star().to_deterministic().minimize()
        )

    else:
        worked = get_target_type(worked, "regex")
        result = MemBox(False, "regex", worked.value.kleene_star())

    return result


def concatenate(first, second):
    allow_types = ["dfa", "regex", "str"]
    f_worked = first
    s_worked = second

    if type(first) == str:
        f_worked = MemBox(False, "str", first)
    if type(second) == str:
        s_worked = MemBox(False, "str", second)

    if type(f_worked) != MemBox or type(s_worked) != MemBox:
        raise InterpError(["concatenate func"], "Args are not in correct internal type")
    if (
        f_worked.v_type not in allow_types
        or s_worked.v_type not in allow_types
        or f_worked.is_list
        or s_worked.is_list
    ):
        raise InterpError(
            ["concatenate func"], "Args are not in allowed type for operation"
        )

    if f_worked.v_type == "dfa" or s_worked.v_type == "dfa":
        f_worked = get_target_type(f_worked, "dfa")
        s_worked = get_target_type(s_worked, "dfa")
        result = MemBox(False, "dfa", f_worked.value.concatenate(s_worked.value))

    else:
        f_worked = get_target_type(f_worked, "regex")
        s_worked = get_target_type(s_worked, "regex")
        result = MemBox(False, "regex", f_worked.value.concatenate(s_worked.value))

    return result


def union(first, second):
    allow_types = ["dfa", "regex", "str"]
    f_worked = first
    s_worked = second

    if type(first) == str:
        f_worked = MemBox(False, "str", first)
    if type(second) == str:
        s_worked = MemBox(False, "str", second)

    if type(f_worked) != MemBox or type(s_worked) != MemBox:
        raise InterpError(["union func"], "Args are not in correct internal type")
    if (
        f_worked.v_type not in allow_types
        or s_worked.v_type not in allow_types
        or f_worked.is_list
        or s_worked.is_list
    ):
        raise InterpError(["union func"], "Args are not in allowed type for operation")

    if f_worked.v_type == "dfa" or s_worked.v_type == "dfa":
        f_worked = get_target_type(f_worked, "dfa")
        s_worked = get_target_type(s_worked, "dfa")
        result = MemBox(False, "dfa", f_worked.value.union(s_worked.value))

    else:
        f_worked = get_target_type(f_worked, "regex")
        s_worked = get_target_type(s_worked, "regex")
        result = MemBox(False, "regex", f_worked.value.union(s_worked.value))

    return result


def intersection(first, second):
    allow_types = ["dfa", "regex", "str"]
    f_worked = first
    s_worked = second

    if type(first) == str:
        f_worked = MemBox(False, "regex", Regex(first))
    if type(second) == str:
        s_worked = MemBox(False, "regex", Regex(second))

    if type(f_worked) != MemBox or type(s_worked) != MemBox:
        raise InterpError(
            ["intersection func"], "Args are not in correct internal type"
        )
    if (
        f_worked.v_type not in allow_types
        or s_worked.v_type not in allow_types
        or f_worked.is_list
        or s_worked.is_list
    ):
        raise InterpError(
            ["intersection func"], "Args are not in allowed type for operation"
        )

    elif f_worked.v_type == "dfa" or s_worked.v_type == "dfa":
        f_worked = get_target_type(f_worked, "dfa")
        s_worked = get_target_type(s_worked, "dfa")
        result = MemBox(False, "dfa", f_worked.value.get_intersection(s_worked.value))

    else:
        f_worked = get_target_type(f_worked, "regex")
        s_worked = get_target_type(s_worked, "regex")
        f_enfa = f_worked.value.to_epsilon_nfa()
        s_enfa = s_worked.value.to_epsilon_nfa()
        res_dfa = f_enfa.get_intersection(s_enfa).to_deterministic().minimize()
        res_regex = res_dfa.to_regex()
        result = MemBox(False, "regex", res_regex)

    return result
