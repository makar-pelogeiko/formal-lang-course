import pytest
from project.parser.parser_invoker import write_to_dot

path = "D:\\projects\\gitproj\\formal-lang-course\\tests\data\\parsed_grammar.dot"


def test_write_to_dot():
    line = """let Ig1 = load graph 'wine'
let Ig1 = load graph from 'home/wine.dot'
let Iquery1 = ('type' || Il1)**\n"""
    status = write_to_dot(line, path)
    obtained = open(path, "r")

    path_expected = "D:\\projects\\gitproj\\formal-lang-course\\tests\data\\parsed_grammar_expected.dot"
    expected = open(path_expected, "r")
    assert (expected.read() == obtained.read()) and status


def test_incorrect_text():
    line = """let Ig1 let = load graph 'wine'
let Ig1 = load graph from 'home/wine.dot'
let Iquery1 = ('type' || Il1)**\n"""
    status = write_to_dot(line, path)

    assert status == False
