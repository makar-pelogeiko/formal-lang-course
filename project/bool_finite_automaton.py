from scipy.sparse import kron
from scipy.sparse import dok_matrix
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State


class BoolFiniteAutomaton:
    def __init__(self):
        self.alphabet = {}
        self.bool_matrices = {}
        self.states_dict = {}
        self.start_states = set()
        self.final_states = set()

    @classmethod
    def bool_matrices_from_nfa(cls, nfa_in):
        """
        :param nfa_in: NondeterministicFiniteAutomaton
        :return: MatrixTransform from nfa_in
        """
        first_dict = nfa_in.to_dict()
        first_prim_keys = first_dict.keys()
        states_dict = {state: index for index, state in enumerate(nfa_in.states)}
        alphabet = nfa_in.symbols
        bool_matrices = {}
        for symbol in alphabet:
            matrix = dok_matrix((len(nfa_in.states), len(nfa_in.states)), dtype=bool)
            for state in first_prim_keys:
                if symbol in set(first_dict[state].keys()):
                    if isinstance(first_dict[state][symbol], set):
                        for point in list(first_dict[state][symbol]):
                            matrix[states_dict[state], states_dict[point]] = True
                    else:
                        matrix[
                            states_dict[state], states_dict[first_dict[state][symbol]]
                        ] = True
            bool_matrices[symbol] = matrix
        obj = cls()
        obj.start_states = nfa_in.start_states
        obj.final_states = nfa_in.final_states
        obj.alphabet = alphabet
        obj.bool_matrices = bool_matrices
        obj.states_dict = states_dict
        return obj

    def get_nfa(self):
        """
        This function builds NondeterministicFiniteAutomaton from object BoolFiniteAutomaton
        :return: NondeterministicFiniteAutomaton
        """
        nfa_result = NondeterministicFiniteAutomaton()
        # create all transitions from several bool matrix
        for symbol in self.alphabet:
            for i, j in zip(*self.bool_matrices[symbol].nonzero()):
                nfa_result.add_transition(State(i), symbol, State(j))
        # find and define start states of NFA
        for st in self.start_states:
            nfa_result.add_start_state(st)
        for st in self.final_states:
            nfa_result.add_final_state(st)
        return nfa_result

    def intersect(self, snd_bool_auto):
        """
        this function crosses 2 nfa (dfa can be passed as second_auto)
        :param snd_bool_auto: BoolFiniteAutomaton from graph or nfa
        :return: NondeterministicFiniteAutomaton, dictionary-
        decomposed result matrix(dict key - symbol, value sparse csr_matrix)
        """
        result_bools = {}
        result_alphabet = self.alphabet & snd_bool_auto.alphabet
        # not a list, but a dictionary
        for i in result_alphabet:
            result_bools[i] = kron(
                self.bool_matrices[i], snd_bool_auto.bool_matrices[i], format="csr"
            )
        # build a nfa (BoolFiniteAutomaton) from several bool matrix
        obj = BoolFiniteAutomaton()
        # find and define start states of NFA
        for fst_start in self.start_states:
            for snd_start in snd_bool_auto.start_states:
                id_fst = self.states_dict[fst_start]
                id_snd = snd_bool_auto.states_dict[snd_start]
                obj.start_states.add(
                    State(len(snd_bool_auto.states_dict) * id_fst + id_snd)
                )
        # find and define final states of NFA
        for fst_final in self.final_states:
            for snd_finale in snd_bool_auto.final_states:
                id_fst = self.states_dict[fst_final]
                id_snd = snd_bool_auto.states_dict[snd_finale]
                obj.final_states.add(
                    State(len(snd_bool_auto.states_dict) * id_fst + id_snd)
                )
        obj.alphabet = result_alphabet
        obj.bool_matrices = result_bools
        obj.states_dict = {
            State(index): index
            for index in (0, result_bools[next(iter(result_alphabet))].shape[0])
        }
        return obj

    @staticmethod
    def transitive_closure(matrix):
        """
        :param matrix: sparse matrix
        :return: transitive clause sparse matrix
        """
        prev_nnz = matrix.nnz
        curr_nnz = 0
        while prev_nnz != curr_nnz:
            matrix += matrix @ matrix
            prev_nnz, curr_nnz = curr_nnz, matrix.nnz
        return matrix
