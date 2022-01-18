from scipy.sparse import kron
from scipy.sparse import dok_matrix
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from pyformlang.cfg import Variable
from project.rsm_utils.rsm import RSM
from project.rsm_utils.rsm_box import Box


class BoolRSMAutomaton:
    """
    :raise Exception("empty alphabet") if intersection alphabet is empty
    """

    def __init__(self):
        self.alphabet = {}
        self.num_states = 0
        self.bool_matrices = {}
        self.states_dict = dict()
        self.start_states = set()
        self.final_states = set()
        self.variables_of_start_final_states = {}

    def _rename_rsm_box_state(self, box_var: Variable, state: State):
        return State(f"""{box_var.value}#{state.value}""")

    @classmethod
    def from_rsm(cls, rsm):
        bool_rsm = cls()
        bool_rsm.num_states = sum(len(box.dfa.states) for box in rsm.boxes.values())

        box_indificator = 0
        for box in rsm.boxes.values():
            for idx, state in enumerate(box.dfa.states):
                name_uniq = bool_rsm._rename_rsm_box_state(box.variable, state)
                bool_rsm.states_dict[name_uniq] = box_indificator + idx

                if state in box.dfa.start_states:
                    bool_rsm.start_states.add(bool_rsm.states_dict[name_uniq])
                if state in box.dfa.final_states:
                    bool_rsm.final_states.add(bool_rsm.states_dict[name_uniq])

            box_indificator += len(box.dfa.states)

            for state in box.dfa.final_states:
                bool_rsm.variables_of_start_final_states[
                    (
                        bool_rsm.states_dict[
                            bool_rsm._rename_rsm_box_state(
                                box.variable, box.dfa.start_state
                            )
                        ],
                        bool_rsm.states_dict[
                            bool_rsm._rename_rsm_box_state(box.variable, state)
                        ],
                    )
                ] = box.variable.value

            bool_rsm.bool_matrices.update(bool_rsm._create_box_bool_matrices(box))
        return bool_rsm

    @classmethod
    def from_automaton(cls, automaton):
        """
        :param automaton: DFA or NFA
        :return: BoolRSMAutomaton representation
        """
        bool_res = cls()
        bool_res.num_states = len(automaton.states)
        bool_res.start_states = automaton.start_states
        bool_res.final_states = automaton.final_states
        bool_res.states_dict = {
            state: idx for idx, state in enumerate(automaton.states)
        }

        temp_matrices = {}
        for st_from, trans in automaton.to_dict().items():
            for label, states_to in trans.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for st_to in states_to:
                    idx_from = bool_res.states_dict[st_from]
                    idx_to = bool_res.states_dict[st_to]
                    label = str(label)
                    if label not in temp_matrices:
                        temp_matrices[label] = dok_matrix(
                            (bool_res.num_states, bool_res.num_states), dtype=bool
                        )
                    temp_matrices[label][idx_from, idx_to] = True

        bool_res.bool_matrices = temp_matrices
        return bool_res

    def _create_box_bool_matrices(self, box: Box):
        bool_matrices = {}
        for s_from, trans in box.dfa.to_dict().items():
            for label, states_to in trans.items():
                label = str(label)
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for s_to in states_to:
                    idx_from = self.states_dict[
                        self._rename_rsm_box_state(box.variable, s_from)
                    ]
                    idx_to = self.states_dict[
                        self._rename_rsm_box_state(box.variable, s_to)
                    ]

                    if label in self.bool_matrices:
                        self.bool_matrices[label][idx_from, idx_to] = True
                        continue
                    if label not in bool_matrices:
                        bool_matrices[label] = dok_matrix(
                            (self.num_states, self.num_states), dtype=bool
                        )
                    bool_matrices[label][idx_from, idx_to] = True

        return bool_matrices

    def transitive_closure(
        self,
    ):
        """
        :return: transitive clause sparse matrix
        """

        if self.bool_matrices.values():
            matrix = sum(self.bool_matrices.values())
        else:
            return dok_matrix((self.num_states, self.num_states), dtype=bool)

        prev_nnz = matrix.nnz
        curr_nnz = 0

        while prev_nnz != curr_nnz:
            matrix += matrix @ matrix
            prev_nnz, curr_nnz = curr_nnz, matrix.nnz
        return matrix

    def intersect(self, other: "BoolRSMAutomaton"):
        """
        !There is No dict() variables_of_start_final_states - it is not needed!
        !There is dict with doubled values, do not need to rename states into strings!
        first - matrices of this object
        :param other:  second - matrices of other object
        :return: Kroneker products of matrices from first and second with same labels
        """
        bool_res = self.__class__()
        bool_res.num_states = self.num_states * other.num_states
        common_labels = self.bool_matrices.keys() & other.bool_matrices.keys()

        for label in common_labels:
            bool_res.bool_matrices[label] = kron(
                self.bool_matrices[label], other.bool_matrices[label]
            )

        for st_fst, st_fst_idx in self.states_dict.items():
            for st_snd, st_snd_idx in other.states_dict.items():
                new_state = new_state_idx = st_fst_idx * other.num_states + st_snd_idx
                bool_res.states_dict[new_state] = new_state_idx

                if st_fst in self.start_states and st_snd in other.start_states:
                    bool_res.start_states.add(new_state)

                if st_fst in self.final_states and st_snd in other.final_states:
                    bool_res.final_states.add(new_state)

        return bool_res
