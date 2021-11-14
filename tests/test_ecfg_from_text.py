import pytest
from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex
from project.ecfg_utils.ecfg import ECFG
from project.regexp_dfa import dfa_from_regexp

# TODO No stabylity in Regex compare, but regex are always right


@pytest.mark.parametrize(
    "text_ecfg, expect_prod",
    [
        ("""""", {}),
        (
            """S -> a S b | #epsilon#""",
            {
                Variable("S"): Regex("a S b S | #epsilon#"),
            },
        ),
        ("""S -> (a | b)* c""", {Variable("S"): Regex("(a | b)* c")}),
        (
            """
         S -> (a (S | b) c)*
         A -> a b c
         """,
            {
                Variable("S"): Regex("(a (S | b) c)*"),
                Variable("A"): Regex("a b c"),
            },
        ),
    ],
)
def test_read_from_text(text_ecfg, expect_prod):
    ecfg = ECFG.from_text(text_ecfg)

    for key in ecfg.productions.keys():
        e_prod = ecfg.productions[key]
        # Can not simply compare Regex(), so will compare nfa equivalent to Regex
        dfa_exp = dfa_from_regexp(expect_prod[key])
        dfa_occur = dfa_from_regexp(e_prod.body)
        equiv = dfa_exp.is_equivalent_to(dfa_occur)
        assert key == e_prod.head and equiv

    assert expect_prod.keys() == ecfg.productions.keys()
