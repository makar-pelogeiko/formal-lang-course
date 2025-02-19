import sys

import project.console
from project.console import *

import project.graph_utils
from project.graph_utils import *

import project.regexp_dfa
from project.regexp_dfa import *

import project.graph_nfa
from project.graph_nfa import *

import project.bool_finite_automaton
from project.bool_finite_automaton import *

if sys.platform.startswith("linux"):
    import project.bool_finite_automaton_cubool
    from project.bool_finite_automaton_cubool import *

import project.rpq
from project.rpq import *

import project.cfg.cfg_normal_form
from project.cfg.cfg_normal_form import *

import project.cyk_algo
from project.cyk_algo import *
