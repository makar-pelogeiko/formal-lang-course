import pytest
from project.cyk_algo import cyk
from pyformlang.cfg import CFG


@pytest.mark.parametrize(
    "cfg, word_lst",
    [
        (
            """
            S -> epsilon
            """,
            ["", "not in grammar"],
        ),
        (
            """
            S -> a
            """,
            ["a", "not in grammar", "b"],
        ),
        (
            """
            S -> S S
            s -> a S b
            S -> c S d
            S -> epsilon
            """,
            ["", "ab", "aabbcd", "not in grammar", "abcdef"],
        ),
    ],
)
def test_cyk(cfg, word_lst):
    cfg = CFG.from_text(cfg)
    for word in word_lst:
        assert cyk(cfg, word) == cfg.contains(word)
