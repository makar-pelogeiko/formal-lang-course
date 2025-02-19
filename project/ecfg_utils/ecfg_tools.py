"""Function and Tools for working with Extended Context Free Grammar"""
from pyformlang.cfg import CFG
from pyformlang.regular_expression import Regex
from project.ecfg_utils.ecfg import ECFG
from project.ecfg_utils.ecfg_production import ECFGProduction
from project.regexp_dfa import dfa_from_regexp
from project.rsm_utils.rsm import RSM
from project.rsm_utils.rsm_box import Box
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol


def cfg_to_ecfg(cfg: CFG):
    """
    Convert a Context Free Grammar to an Extended Context Free Grammar
    :param cfg:
    :return: ECFG object
    """
    productions = dict()

    for production in cfg.productions:
        body_lst = [prod_item.value for prod_item in production.body]

        if production.body:
            body_str = " ".join(body_lst)
        else:
            # TODO: body_str = "" - try this or this body_str = "#epsilon#"
            body_str = ""

        body = Regex(body_str)

        if production.head not in productions.keys():
            productions[production.head] = body
        else:
            productions[production.head] = productions[production.head].union(body)

    ecfg_productions = {
        head: ECFGProduction(head, body) for head, body in productions.items()
    }

    return ECFG(cfg.variables, cfg.start_symbol, ecfg_productions)


def ecfg_to_rsm(ecfg: ECFG) -> RSM:
    """Convert an Extended Context Free Grammar to a Recursive State Machine"""
    boxes = dict()
    for id, production in enumerate(ecfg.productions.values()):
        dfa = dfa_from_regexp(production.body)
        if dfa.is_empty():
            dfa.add_start_state(State(0))
            dfa.add_final_state(State(0))
        boxes[id] = Box(production.head, dfa)

    return RSM(start_symbol=ecfg.start_symbol, boxes=boxes)


def ecfg_from_file(path: str, start_symbol: str = "S"):
    """Read an Extended Context Free Grammar from a file
    :returns ECFG object or None (if an exception occurred)"""
    try:
        file = open(path, "r")
        text_cfg = file.read()
        file.close()
    except:
        print("can not open and read file")

    ecfg = None
    try:
        ecfg = ECFG.from_text(text_cfg, start_symbol=start_symbol)
    except:
        print("not a cfg syntax in file")
        ecfg = None
    return ecfg
