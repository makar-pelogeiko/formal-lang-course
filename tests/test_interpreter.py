import pytest
from project.interpreter_gql.interpreter import GQLInterpreter


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
            """let Ig1 = load graph 'tests/data/graph1.dot'\n
print get labels of (Ig1)\n""",
            [">>>{b, a}", ">>>{a, b}"],
        ),
        (
            """let Ig1 = load graph 'tests/data/graph1.dot'\n
let Ig2 = set start of (Ig1) to get starts of ( Ig1 )\n
let st = get finals of (Ig1)\n
print filter (fun (df) -> df in {'0', '3;2', '4',})(st)\n""",
            [">>>{'0', '4'}", ">>>{'4', '0'}"],
        ),
        (
            """print 'a' && ('b' || 'a')**\n""",
            [">>>($.a)"],
        ),
        (
            """let Ig1 = load graph 'tests/data/graph1.dot'\n
print Ig1 && 'a b b'\n""",
            [">>>($.((a.b).b))", ">>>($.(a.(b.b)))"],
        ),
        (
            """let Ig1 = load graph 'tests/data/graph1.dot'\n
let Ig2 = set start of (Ig1) to get starts of ( Ig1 )\n
let st = get finals of (Ig1)\n
let query = ('b')** || 'a' || 'a b'\n
let inter = Ig1 && query\n
print inter && 'a b'\n""",
            [">>>($.(a.b))"],
        ),
        (
            """let Ig1 = load graph 'tests/data/graph1.dot'\n
let Ig2 = set start of (Ig1) to get starts of ( Ig1 )\n
print Ig2 && 'a b'\n""",
            [">>>($.(a.b))"],
        ),
        (
            """let Ig1 = load graph 'tests/data/graph1.dot'\n
let ff = get reachable of (Ig1)\n
print filter (fun (df) -> df[1] in {0,})(filter (fun (df) -> df[0] in {1, 2,})(ff))\n""",
            [">>>{(1, 0), (2, 0)}", ">>>{(2, 0), (1, 0)}", ">>>set()"],
        ),
        (
            """let Ig1 = load graph 'tests/data/graph1.dot'\n
print filter (fun (df) -> df in {'0',})(get finals of (Ig1))\n""",
            [">>>{'0'}"],
        ),
    ],
)
def test_multiple_functions(input_, expect_output):
    for i in range(4):
        test_interp = GQLInterpreter()
        test_interp.run_query(input_)
        answer = test_interp.visitor.output_logger

        result = False
        for out in expect_output:
            result = answer == out
            if result:
                break
        if result:
            break

    assert result


@pytest.mark.parametrize(
    "input_, expect_output",
    [
        (
            """print get labels of (Ig1)\n""",
            [
                "----Exception----",
                "No value with name: Ig1",
                "-----------------",
                "memory call",
                "var expr pure",
                "expr var",
                "expr get_labels",
                "print statement: [printget labels of (Ig1)]",
                "-----------------",
            ],
        ),
        (
            "let Ig1 = load graph 'sssgraph1.dot'\n",
            [
                "----Exception----",
                "Can not load graph: sssgraph1.dot",
                "-----------------",
                "expr load",
                "bind statement: [Ig1]",
                "-----------------",
            ],
        ),
        (
            """let st = get finals of (Ig1)\n
let Ig1 = load graph 'tests/data/graph1.dot'\n""",
            [
                "----Exception----",
                "No value with name: Ig1",
                "-----------------",
                "memory call",
                "var expr pure",
                "expr var",
                "expr get_final",
                "bind statement: [st]",
                "-----------------",
            ],
        ),
    ],
)
def test_errors(input_, expect_output):
    test_interp = GQLInterpreter()
    test_interp.run_query(input_)
    answer = test_interp.out_log_list

    assert answer == expect_output


@pytest.mark.parametrize(
    "input_, expect_output",
    [
        (
            "print get starts of (load graph 'tests/data/graph1.dot')\n",
            ">>>{0;1;2;3;4;5}",
        ),
    ],
)
def test_multi_single_command(input_, expect_output):
    test_interp = GQLInterpreter()
    test_interp.run_query(input_)
    answer = test_interp.visitor.output_logger

    assert answer == expect_output
