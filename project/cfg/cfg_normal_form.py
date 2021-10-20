from pyformlang.cfg import CFG, Production

__all__ = ["cfg_to_cnf", "cfg_from_file"]


def cfg_to_cnf(cfg: CFG) -> CFG:
    """
    Takes context free grammar and return chomsky normal form of it
    :param cfg: context free grammar (pyformlang.cfg.CFG)
    :return: cfg in chomsky normal form (pyformlang.cfg.CFG)
    WARNING: chomsky normal form standart function has no way to accept epsilon words
    """
    cnf = cfg.to_normal_form()
    if cfg.generate_epsilon():
        cnf._productions.add(Production(cnf.start_symbol, []))
    return cnf


def cfg_from_file(path: str, start_symbol: str = "S"):
    """
    Reads context free grammar from file (path) with start symbol (common 'S')
    and returns this grammar in pyformlang.cfg.CFG type
    :param path: str, string with full path to file
    :param start_symbol: str, string that represents start nonterminal symbol of grammar
    :return: CFG, context free grammar
    """
    try:
        file = open(path, "r")
        text_cfg = file.read()
        file.close()
    except:
        print("can not open and read file")

    cfg = None
    try:
        cfg = CFG.from_text(text_cfg, start_symbol=start_symbol)
    except:
        print("not a cfg syntax in file")
        cfg = CFG()
    return cfg
