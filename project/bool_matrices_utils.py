from scipy.sparse import kron
from scipy.sparse import lil_matrix, csr_matrix
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State


class BoolMatricesGroup:
    def __init__(self):
        self.alphabet = {}
        self.bool_matrices = {}
        self.states_dict = {}
        self.states_invert_dict = {}
        self.nfa = None

    @classmethod
    def bool_matrices_from_nfa(cls, nfa_in):
        """
        :param nfa_in: NondeterministicFiniteAutomaton
        :return: MatrixTransform from nfa_in
        """
        first_dict = nfa_in.to_dict()
        first_prim_keys = first_dict.keys()
        states_dict = {state: index for index, state in enumerate(nfa_in.states)}
        states_invert_dict = {index: state for index, state in enumerate(nfa_in.states)}
        temp_list = []
        for i in first_prim_keys:
            temp_list = temp_list + list(first_dict[i].keys())
        alphabet = set(temp_list)
        bool_matrices = {}
        for symbol in alphabet:
            matrix = lil_matrix((len(nfa_in.states), len(nfa_in.states)))
            for state in first_prim_keys:
                if symbol in set(first_dict[state].keys()):
                    if isinstance(first_dict[state][symbol], set):
                        for point in list(first_dict[state][symbol]):
                            # matrix[int(f"""{state}"""), int(f"""{point}""")] = 1
                            matrix[states_dict[state], states_dict[point]] = 1
                    else:
                        matrix[
                            states_dict[state], states_dict[first_dict[state][symbol]]
                        ] = 1
            bool_matrices[symbol] = matrix
        obj = cls()
        obj.nfa = nfa_in
        obj.alphabet = alphabet
        obj.bool_matrices = bool_matrices
        obj.states_dict = states_dict
        obj.states_invert_dict = states_invert_dict
        return obj

    def cross_automats(self, second_auto: NondeterministicFiniteAutomaton):
        """
        this function crosses 2 nfa (dfa can be passed as second_auto)
        :param second_auto:
        NondeterministicFiniteAutomaton (may be FiniteAutomato)
        :return: NondeterministicFiniteAutomaton, dictionary-
        decomposed result matrix(dict key - symbol, value sparse csr_matrix)
        """
        snd_set = BoolMatricesGroup.bool_matrices_from_nfa(second_auto)
        result_bools = {}
        result_alphabet = self.alphabet & snd_set.alphabet
        # not a list, but a dictionary
        for i in result_alphabet:
            temp_result = kron(
                self.bool_matrices[i], snd_set.bool_matrices[i], format="csr"
            )
            result_bools[i] = temp_result
        # build a nfa from several bool matrix
        nfa_result = NondeterministicFiniteAutomaton()
        # create all transitions from several bool matrix
        for symbol in result_alphabet:
            for i in range(0, result_bools[symbol].shape[0]):
                for j in range(0, result_bools[symbol].shape[0]):
                    if (result_bools[symbol])[i, j] == 1:
                        nfa_result.add_transition(State(i), symbol, State(j))
        # find and define start states of NFA
        for fst_start in self.nfa.start_states:
            for snd_start in second_auto.start_states:
                id_fst = self.states_dict[fst_start]
                id_snd = snd_set.states_dict[snd_start]
                nfa_result.add_start_state(
                    State(len(snd_set.nfa.states) * id_fst + id_snd)
                )
        # find and define finale states of NFA
        for fst_finale in self.nfa.final_states:
            for snd_finale in second_auto.final_states:
                id_fst = self.states_dict[fst_finale]
                id_snd = snd_set.states_dict[snd_finale]
                nfa_result.add_final_state(
                    State(len(snd_set.nfa.states) * id_fst + id_snd)
                )
        return nfa_result, result_bools
