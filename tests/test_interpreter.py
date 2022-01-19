import pytest
from project.interpreter_gql.interpreter import GQLInterpreter


@pytest.fixture
def graph():
    return GQLInterpreter()


@pytest.mark.parametrize(
    "input_, expect_output",
    [
        (
            "print 12\n",
            [">>>12"],
        ),
        (
            "print filter (fun (df) -> df in {1, 2, 34,})({1, 2, 3, 4,})\n",
            [">>>{'1', '2'}", ">>>{'2', '1'}"],
        ),
        ("print ('last')**\n", [">>>(last)*"]),
        ("print 'type' || 'last'\n", [">>>(type|last)"]),
        ("print 'last' && 'type'\n", [">>>Empty"]),
        ("print 'last' && 'last'\n", [">>>($.last)"]),
        (
            "print map (fun (df) -> 44 * df)({1, 2,})\n",
            [">>>{'88', '44'}", ">>>{'44', '88'}"],
        ),
    ],
)
def test_atomic_functions(input_, expect_output):
    test_interp = GQLInterpreter()
    test_interp.run_query(input_)
    answer = test_interp.visitor.output_logger

    result = False
    for out in expect_output:
        result = answer == out
        if result:
            break

    assert result


@pytest.mark.parametrize(
    "input_, expect_output",
    [
        (
            "print get labels of (Ig1)\n",
            [">>>{b, a}", ">>>{a, b}"],
        ),
        (
            "print filter (fun (df) -> df in {'0', '3;2', '4',})(st)\n",
            [">>>{'0', '4'}", ">>>{'4', '0'}"],
        ),
        (
            "print 'a' && ('b' || 'a')**\n",
            [">>>($.a)"],
        ),
        ("print Ig1 && 'a b b'\n", [">>>($.((a.b).b))", ">>>($.(a.(b.b)))"]),
        ("print inter && 'a b'\n", [">>>($.(a.b))"]),
        ("print Ig2 && 'a b'\n", [">>>($.(a.b))"]),
    ],
)
def test_multiple_functions(input_, expect_output):
    test_interp = GQLInterpreter()
    test_interp.run_query(
        "let Ig1 = load graph 'D:\\projects\\gitproj\\formal-lang-course\\tests\\data\\graph1.dot'\n"
    )
    test_interp.run_query("let Ig1 = load graph 'tests/data/graph1.dot'\n")

    test_interp.run_query("let Ig2 = set start of (Ig1) to get starts of ( Ig1 )\n")
    test_interp.run_query("let st = get finals of (Ig1)\n")
    test_interp.run_query("let query = ('b')** || 'a' || 'a b'\n")
    test_interp.run_query("let inter = Ig1 && query\n")
    test_interp.run_query(input_)
    answer = test_interp.visitor.output_logger

    result = False
    for out in expect_output:
        result = answer == out
        if result:
            break

    assert result
