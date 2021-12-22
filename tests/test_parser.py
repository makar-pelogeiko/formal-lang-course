import sys
import pytest

if sys.platform.startswith("linux"):
    from project.parser.parser_invoker import *
else:
    pytest.skip("skipping ubuntu-only tests", allow_module_level=True)


def test_load_text():
    s = parse_to_string("let Ig1 = load graph 'wine'\n")
    assert (
        s
        == "(prog (stm let (var Ig1) = (expr (load load graph (path 'wine')))) \\n <EOF>)"
    )


def test_load_from_text():
    s = parse_to_string("let Ig1 = load graph from 'home/wine.dot'\n")
    assert (
        s
        == "(prog (stm let (var Ig1) = (expr (load load graph from (path 'home/wine.dot')))) \\n <EOF>)"
    )


def test_and_or_star_text():
    s = parse_to_string("let Iquery1 = Il0 && ('type' || Il1)**\n")
    assert (
        s
        == "(prog (stm let (var Iquery1) = (expr (expr (var Il0)) (intersect &&) (expr (star ( (expr (expr (val 'type')) (union ||) (expr (var Il1))) )**)))) \\n <EOF>)"
    )


def test_load_accept():
    s = is_in_grammar("let Ig1 = load graph 'wine'\n")
    assert s == True


def test_load_from_accept():
    s = is_in_grammar("let Ig1 = load graph from 'home/wine.dot'\n")
    assert s == True


def test_and_or_star_accept():
    s = is_in_grammar("let Iquery1 = Il0 && ('type' || Il1)**\n")
    assert s == True


def test_and_or_star_fail():
    s = is_in_grammar("let Ig1 let = load graph 'wine'\n")
    assert s == False
