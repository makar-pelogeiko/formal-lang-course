"""Cocke-Younger-Kasami algorithm"""
from pyformlang.cfg import CFG

__all__ = ["cyk"]


def cyk(cfg: CFG, word: str) -> bool:
    """Check if a Context Free Grammar contains a word (string)"""
    cnf = cfg.to_normal_form()
    word_len = len(word)

    if 0 == word_len:
        return cfg.generate_epsilon()

    term_productions = [p for p in cnf.productions if len(p.body) == 1]
    var_productions = [p for p in cnf.productions if len(p.body) == 2]

    matrix = []
    for i in range(word_len):
        matrix.append([])
        for j in range(word_len):
            matrix[i].append(set())

    for i in range(word_len):
        matrix[i][i].update(
            prod.head.value
            for prod in term_productions
            if word[i] == prod.body[0].value
        )

    for step in range(1, word_len):
        for i in range(word_len - step):
            j = i + step
            for k in range(i, j):
                for prod in var_productions:
                    if (
                        prod.body[0].value in matrix[i][k]
                        and prod.body[1].value in matrix[k + 1][j]
                    ):
                        matrix[i][j].update(prod.head.value)

    return cnf.start_symbol.value in matrix[0][word_len - 1]
