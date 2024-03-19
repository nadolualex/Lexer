from typing import List, Tuple, Union
from src.NFA import NFA
from src.DFA import DFA
from src.Regex import parse_regex, CreateNFA

class Lexer:
    def __init__(self, spec: List[Tuple[str, str]]) -> None:
        self.state_token = {}
        self.token_pos = {}
        self.index = []
        self.list_token = []
        self.dfa = DFA(set(), set(), 0, {}, set())

        self._build_dfa(spec)

    def _build_dfa(self, spec: List[Tuple[str, str]]) -> None:
        new_nfa = CreateNFA()
        new_nfa.q0 = 0
        new_nfa.K = {0}
        new_nfa.d[0, ''] = set()

        for i, (token, regex_str) in enumerate(spec):
            regex = parse_regex(regex_str)
            regex_nfa = regex.thompson()

            new_nfa.d.update(regex_nfa.d)
            new_nfa.S.update(regex_nfa.S)
            new_nfa.K.update(regex_nfa.K)
            new_nfa.F.update(regex_nfa.F)

            new_nfa.d[0, ''].update(regex_nfa.F)
            for final_state in regex_nfa.F:
                self.state_token[final_state] = token

            self.token_pos[token] = i
            self.index.append(0)
            self.list_token.append(token)

        final_nfa = NFA(new_nfa.S, new_nfa.K, new_nfa.q0, new_nfa.d, new_nfa.F)
        self.dfa = final_nfa.subset_construction()

    def lex(self, word: str) -> Union[List[Tuple[str, str]], List[Tuple[str, str]]]:
        state = self.dfa.q0
        i = 0
        j = 0
        line = 0
        last_new_line = -1
        final_list = []

        for k in range(len(self.index)):
            self.index[k] = -1

        val_max = -1
        ind_max = -1

        while i < len(word):
            j = i
            while j < len(word):
                if word[j] == '\n' and last_new_line != j:
                    line += 1
                    last_new_line = j

                if state in self.dfa.F:
                    states = map(int, filter(None, (i.strip() for i in state.split('q'))))
                    for q in states:
                        if q in self.state_token:
                            index_pos = self.token_pos[self.state_token[q]]
                            self.index[index_pos] = j
                            if j > val_max or (j == val_max and index_pos < ind_max):
                                val_max = j
                                ind_max = index_pos

                if (state, word[j]) in self.dfa.d:
                    state = self.dfa.d[(state, word[j])]
                else:
                    aux = "No viable alternative at character " + str(j - last_new_line - 1) + ", line " + str(line)
                    return [('', aux)]

                if state == "sink":
                    if val_max == -1:
                        if j == len(word) - 1:
                            aux = "No viable alternative at character EOF, line " + str(line)
                        else:
                            aux = "No viable alternative at character " + str(j - last_new_line - 1) + ", line " + str(line)
                        return [('', aux)]

                    final_list.append((self.list_token[ind_max], word[i:self.index[ind_max]]))
                    i = self.index[ind_max]
                    state = self.dfa.q0
                    for k in range(len(self.index)):
                        self.index[k] = -1
                    val_max = -1
                    ind_max = -1
                    break
                else:
                    j += 1
                    if j == len(word):
                        if state in self.dfa.F:
                            states = map(int, filter(None, (i.strip() for i in state.split('q'))))
                            for q in states:
                                if q in self.state_token:
                                    index_pos = self.token_pos[self.state_token[q]]
                                    self.index[index_pos] = j
                                    if j > val_max or (j == val_max and index_pos < ind_max):
                                        val_max = j
                                        ind_max = index_pos

                        if val_max == -1:
                            aux = "No viable alternative at character EOF, line " + str(line)
                            return [('', aux)]

                        final_list.append((self.list_token[ind_max], word[i:self.index[ind_max]]))
                        i = self.index[ind_max]

                        if i == len(word):
                            break

                        state = self.dfa.q0
                        for k in range(len(self.index)):
                            self.index[k] = -1
                        val_max = -1
                        ind_max = -1
        return final_list
