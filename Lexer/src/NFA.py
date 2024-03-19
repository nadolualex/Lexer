from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs
SINK_STATE = frozenset()

@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        # compute the epsilon closure of a state (you will need this for subset construction)
        # see the EPSILON definition at the top of this file
        # print the inputs

        # print("alphabet ", self.S)
        # print("states ", self.K)
        # print("initial state ", self.q0)
        # print("functie de tranzitie: dictionar ", self.d)
        # print("final states ", self.F)

        my_set = set()
        stack = [state]

        while len(stack):
            my_state = stack.pop()
            if my_state not in my_set:
                my_set.add(my_state)
                if (my_state, EPSILON) in self.d:
                    for next_state in self.d[(my_state, EPSILON)]: # Check state's successors on epsilon
                        stack.append(next_state)
        return my_set

    def subset_construction(self) -> DFA[frozenset[STATE]]:
        # convert this nfa to a dfa using the subset construction algorithm
        # self.S.add(EPSILON) # Modify this !!!!!!!!!!!!!!!!!!
        DFA.d = dict()
        dfa_first_state = frozenset(self.epsilon_closure(self.q0))
        DFA.K = set()
        next_state = set()
        DFA.F = frozenset()

        #print(DFA.F)

        DFA.q0 = dfa_first_state
        #print(self)
        DFA.K.add(dfa_first_state)

        stack = [dfa_first_state]

        while len(stack):
            #print(" My STACK :" , stack)
            my_state = stack.pop()
            for transitions in self.S:
                for state in my_state:
                    if (state, transitions) in self.d:
                        next_state.update(self.d[(state, transitions)])
                        for element in self.d[(state,transitions)]:
                            #print ( " element : ", element)
                            if len(self.epsilon_closure(element)) > 1:
                                next_state.update(self.epsilon_closure(element))
                #print(" State ", my_state, " goes to state ", next_state,
                      #" on transition ", transitions)
                next_state_frozen = frozenset(next_state)
                next_state = set()
                DFA.d[(my_state, transitions)] = next_state_frozen
                #print(next_state_frozen)
                if next_state_frozen not in DFA.K:
                    DFA.K.add(next_state_frozen)
                    stack.append(next_state_frozen)

        for state in DFA.K:
            if state & frozenset(self.F):
                DFA.F = frozenset(DFA.F.union({state}))

        dfa = DFA(self.S, DFA.K, DFA.q0, DFA.d, DFA.F)

        #print(dfa.S)
        #print(dfa.K)
        #print(dfa.q0)
        #print(dfa.F)

        return dfa
        pass

    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        # optional, but may be useful for the second stage of the project. Works similarly to 'remap_states'
        # from the DFA class. See the comments there for more details.
        # apply function f to all states in the NFA
        new_states = set(f(state) for state in self.K)

        # apply function f to all final states in the NFA
        new_final_states = set(f(state) for state in self.F)

        # apply function f to the initial state in the NFA
        new_q0 = f(self.q0)

        # apply function f to all transitions in the NFA
        new_d = {(f(state), letter): {f(next_state) for next_state in states}
                 for (state, letter), states in self.d.items()}

        return NFA(self.S, new_states, new_q0, new_d, new_final_states)
        pass
