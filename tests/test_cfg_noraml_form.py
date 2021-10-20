import pytest
from pyformlang.cfg import CFG, Production, Variable, Terminal
from project.cfg import cfg_normal_form


# cfg_normal_form.cfg_to_cnf() test
@pytest.mark.parametrize(
    "text_cfg",
    [
        ("S -> a b"),
        ("S -> a b | a S"),
        (
            """S -> a S | b S | F
            F -> c S | d"""
        ),
    ],
)
def test_normal_form_non_epsilon(text_cfg):
    cfg = CFG.from_text(text_cfg)
    cnf = cfg_normal_form.cfg_to_cnf(cfg)
    assert cnf.is_normal_form() and not cnf.generate_epsilon()


@pytest.mark.parametrize(
    "text_cfg",
    [
        ("S -> a b | epsilon"),
        (
            """S -> a S | b S | F
            F -> c S | epsilon"""
        ),
    ],
)
def test_normal_form_with_epsilon(text_cfg):
    cfg = CFG.from_text(text_cfg)
    cnf = cfg_normal_form.cfg_to_cnf(cfg)
    assert not cnf.is_normal_form() and cnf.generate_epsilon()


# cfg_normal_form.cfg_from_file() test
@pytest.mark.parametrize(
    "text_cfg,productions_expected",
    [
        ("not a grammar", set()),
        ("S -> a b", {Production(Variable("S"), [Terminal("a"), Terminal("b")])}),
        (
            """S -> a S | F
            F -> b S | epsilon""",
            {
                Production(Variable("S"), [Variable("F")]),
                Production(Variable("S"), [Terminal("a"), Variable("S")]),
                Production(Variable("F"), []),
                Production(Variable("F"), [Terminal("b"), Variable("S")]),
            },
        ),
    ],
)
def test_read_cfg_from_file(text_cfg, productions_expected):
    f = open("test_cfg.txt", "w")
    f.write(text_cfg)
    f.close()

    cfg = cfg_normal_form.cfg_from_file("test_cfg.txt")
    assert cfg.productions == productions_expected
