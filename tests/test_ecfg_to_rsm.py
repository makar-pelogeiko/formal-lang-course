import pytest
from project.ecfg_utils.ecfg_tools import ecfg_to_rsm, ECFG
from project.regexp_dfa import dfa_from_regexp


@pytest.mark.parametrize(
    """ecfg_text""",
    (
        """
        S -> #epsilon#
        """,
        """
        S -> a S b | B | F
        B -> c B d | S | F
        F -> #epsilon#
        """,
        "",
    ),
)
def test_boxes_regex_equality(ecfg_text):
    ecfg = ECFG.from_text(ecfg_text)
    rsm = ecfg_to_rsm(ecfg)
    ecfg_start_symbol = ecfg.start_symbol
    rsm_start_symbol = rsm.start_symbol
    assert rsm_start_symbol == ecfg_start_symbol
    for key in rsm.boxes.keys():
        assert rsm.boxes[key].variable == key
        assert rsm.boxes[key].dfa.is_equivalent_to(
            dfa_from_regexp(ecfg.productions[key].body)
        )
