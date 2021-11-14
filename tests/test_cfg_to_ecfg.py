import pytest
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex

from project.ecfg_utils.ecfg_tools import cfg_to_ecfg
from project.regexp_dfa import dfa_from_regexp


@pytest.mark.parametrize(
    "cfg, expect_prod",
    [
        (
            "S -> epsilon",
            {Variable("S"): Regex("#epsilon#")},
        ),
        (
            """
                    S -> a S b
                    S -> epsilon
                """,
            {Variable("S"): Regex("(a S b) | #epsilon#")},
        ),
    ],
)
def test_cfg_to_ecfg_correct_productions(cfg, expect_prod):
    ecfg = cfg_to_ecfg(CFG.from_text(cfg))

    for key in ecfg.productions.keys():
        e_prod = ecfg.productions[key]
        # Can not simply compare Regex(), so will compare nfa equivalent to Regex
        dfa_exp = dfa_from_regexp(expect_prod[key])
        dfa_occur = dfa_from_regexp(e_prod.body)
        equiv = dfa_exp.is_equivalent_to(dfa_occur)
        assert key == e_prod.head and equiv

    assert expect_prod.keys() == ecfg.productions.keys()
