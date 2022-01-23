import pytest
import sys
from project.parser.parser_invoker import write_to_dot

if sys.platform.startswith("win"):
    path = "tests\\data\\parsed_grammar.dot"
    path_expected = "tests\\data\\parsed_grammar_expected.dot"
else:
    path = "tests/data/parsed_grammar.dot"
    path_expected = "tests/data/parsed_grammar_expected.dot"


def test_write_to_dot():
    line = """let Ig1 = load graph 'wine'
let Ig1 = load graph from 'home/wine.dot'
let Iquery1 = ('type' || Il1)**\n"""
    status = write_to_dot(line, path)
    obtained = open(path, "r")

    expected = open(path_expected, "r")
    assert (expected.read() == obtained.read()) and status


def test_incorrect_text():
    line = """let Ig1 let = load graph 'wine'
let Ig1 = load graph from 'home/wine.dot'
let Iquery1 = ('type' || Il1)**\n"""
    status = write_to_dot(line, path)

    assert status == False
