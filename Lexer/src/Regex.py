import re
from dataclasses import dataclass
from typing import Dict, Set

from .NFA import NFA, EPSILON


class Regex:
    def thompson(self) -> NFA[int]:
        raise NotImplementedError('the thompson method of the Regex class should never be called')


# you should extend this class with the type constructors of regular expressions and overwrite the 'thompson' method
# with the specific nfa patterns. for example, parse_regex('ab').thompson() should return something like:

# >(0) --a--> (1) -epsilon-> (2) --b--> ((3))

# extra hint: you can implement each subtype of regex as a @dataclass extending Regex

# implement each subtype of regex as a @dataclass extending Regex
class CreateNFA(Regex):
    def thompson(self) -> NFA[int]:
        nfa = NFA(set(), {0}, 0, dict(), set())
        return nfa


@dataclass
class Char(Regex):
    char: str

    def thompson(self) -> NFA[int]:
        # print("self char", self.char)
        nfa = CreateNFA().thompson()
        nfa.S.add(self.char)
        nfa.K.add(0)
        nfa.K.add(1)
        nfa.d[(0, self.char)] = {1}
        nfa.F.add(1)

        # print(" NFA CHAR ", nfa)
        return nfa


@dataclass
class Concat(Regex):
    Left: Regex
    Right: Regex

    def thompson(self) -> NFA[int]:

        nfa_left = self.Left.thompson()
        nfa_right = self.Right.thompson()

        # print("nfa_left before", nfa_left)
        # print("nfa_right before", nfa_right)

        nfa_right = nfa_right.remap_states(lambda x: x + len(nfa_left.K))

        # print("nfa_left after", nfa_left)
        # print("nfa_right after", nfa_right)

        alphabet = nfa_left.S.union(nfa_right.S)
        states = nfa_left.K.union(nfa_right.K)

        start_state = nfa_left.q0
        transition_function = dict()
        transition_function.update(nfa_left.d)
        transition_function.update(nfa_right.d)

        for state in nfa_left.F:
            transition_function[(state, EPSILON)] = {nfa_right.q0}

        final_state = nfa_right.F
        nfa = NFA(alphabet, states, start_state, transition_function, final_state)
        # print(" NFA CONCAT ", nfa)
        return nfa


@dataclass
class Union(Regex):
    Left: Regex
    Right: Regex

    def thompson(self) -> NFA[int]:
        nfa_left = self.Left.thompson()
        nfa_right = self.Right.thompson()

        # print("nfa_left before", nfa_left)
        # print("nfa_right before", nfa_right)

        nfa_left = nfa_left.remap_states(lambda x: x + 1)
        nfa_right = nfa_right.remap_states(lambda x: x + max(nfa_left.K) + 1)

        # print("nfa_left after", nfa_left)
        # print("nfa_right after", nfa_right)

        final_state = max(nfa_left.K.union(nfa_right.K)) + 1

        # print("final_state", final_state)
        alphabet = nfa_left.S.union(nfa_right.S)
        states = {0, final_state}.union(nfa_left.K).union(nfa_right.K)

        start_state = 0

        transitions = dict()

        transitions[(0, EPSILON)] = set()

        # Adaug tranzitiile epsilon de la starea initiala la starile initiale ale celor doua NFA-uri
        transitions[(0, EPSILON)].add(nfa_left.q0)
        transitions[(0, EPSILON)].add(nfa_right.q0)

        transitions.update(nfa_left.d)
        transitions.update(nfa_right.d)

        # Adaug tranzitiile epsilon de la starile finale ale celor doua NFA-uri la starea finala
        for s in nfa_left.F:
            transitions[(s, EPSILON)] = {final_state}

        for s in nfa_right.F:
            transitions[(s, EPSILON)] = {final_state}

        nfa = NFA(alphabet, states, start_state, transitions, F={final_state})

        # print(" NFA UNION ", nfa)
        return nfa


@dataclass
class KleeneStar(Regex):
    Inner: Regex

    def thompson(self) -> NFA[int]:
        nfa_inner = self.Inner.thompson()

        # print("nfa_inner before", nfa_inner)

        nfa_inner = nfa_inner.remap_states(lambda x: x + 1)

        # print("nfa_inner after", nfa_inner)

        final_state = max(nfa_inner.K) + 1

        alphabet = nfa_inner.S
        states = {0, final_state}.union(nfa_inner.K)

        start_state = 0

        transitions = dict()

        transitions[(0, EPSILON)] = set()
        transitions[(0, EPSILON)].add(nfa_inner.q0)
        transitions[(0, EPSILON)].add(final_state)

        transitions.update(nfa_inner.d)

        for s in nfa_inner.F:
            transitions[(s, EPSILON)] = {final_state}
            transitions[(s, EPSILON)].add(nfa_inner.q0)

        nfa = NFA(alphabet, states, start_state, transitions, F={final_state})

        # print(" NFA KLEENE STAR ", nfa)
        return nfa

@dataclass
class QuestionMark(Regex):
    Inner: Regex

    def thompson(self) -> NFA[int]:
        nfa_inner = self.Inner.thompson()

        # print("nfa_inner before", nfa_inner)

        nfa_inner = nfa_inner.remap_states(lambda x: x + 1)

        # print("nfa_inner after", nfa_inner)

        final_state = max(nfa_inner.K) + 1

        alphabet = nfa_inner.S
        states = {0, final_state}.union(nfa_inner.K)

        start_state = 0

        transitions = dict()

        transitions[(0, EPSILON)] = set()
        transitions[(0, EPSILON)].add(nfa_inner.q0)
        transitions[(0, EPSILON)].add(final_state)

        transitions.update(nfa_inner.d)

        for s in nfa_inner.F:
            transitions[(s, EPSILON)] = {final_state}

        nfa = NFA(alphabet, states, start_state, transitions, F={final_state})

        # print(" NFA QUESTION MARK ", nfa)
        return nfa
        pass


@dataclass
class Plus(Regex):
    Inner: Regex

    def thompson(self) -> NFA[int]:
        nfa_inner = self.Inner.thompson()

        # print("nfa_inner before", nfa_inner)

        nfa_inner = nfa_inner.remap_states(lambda x: x + 1)

        # print("nfa_inner after", nfa_inner)

        final_state = max(nfa_inner.K) + 1

        alphabet = nfa_inner.S
        states = {0, final_state}.union(nfa_inner.K)

        start_state = 0

        transitions = dict()

        transitions[(0, EPSILON)] = set()
        transitions[(0, EPSILON)].add(nfa_inner.q0)

        transitions.update(nfa_inner.d)

        for s in nfa_inner.F:
            transitions[(s, EPSILON)] = {final_state}
            transitions[(s, EPSILON)].add(nfa_inner.q0)

        nfa = NFA(alphabet, states, start_state, transitions, F={final_state})

        #print(" NFA PLUS ", nfa)
        return nfa
        pass


@dataclass
class Sugar(Regex):
    char: str

    def thompson(self) -> NFA[int]:
        first_char = self.char[0]

        second_char = self.char[2]

        start_state = 0

        final_state = 1

        alphabet = set()

        states = {0, 1}

        for i in range(ord(first_char), ord(second_char) + 1):
            alphabet.add(chr(i))

        transitions = dict()

        for char in alphabet:
            transitions[(0, char)] = {1}

        nfa = NFA(alphabet, states, start_state, transitions, F={final_state})
        return nfa


def parse_regex(regex: str) -> Regex:
    stack = []
    nfa_left = CreateNFA()
    nfa_right = []

    i = 0
    while i < len(regex):
        # Skip spaces
        if regex[i] == ' ':
            i += 1
            continue

        elif regex[i] == '\n':
            stack.append(Char(regex[i]))

        # Union
        elif regex[i] == '|':
            # Concat
            while stack:
                if nfa_right:
                    nfa_right = Concat(stack.pop(), nfa_right)
                else:
                    nfa_right = stack.pop()

            nfa_left = nfa_right
            right = parse_regex(regex[i + 1:])

            stack.append(right)
            nfa_right = []
            break

        # Plus
        elif regex[i] == '+':
            nfa_right = Plus(nfa_right)

        # Kleene star
        elif regex[i] == '*':
            nfa_right = KleeneStar(nfa_right)

        # Question mark
        elif regex[i] == '?':
            nfa_right = QuestionMark(nfa_right)

        # Parantheses
        elif regex[i] == '(':
            start = i + 1
            end = start
            count_open_parentheses = 1
            while end < len(regex):
                if regex[end] == '(':
                    count_open_parentheses += 1
                elif regex[end] == ')':
                    count_open_parentheses -= 1
                    if count_open_parentheses == 0:
                        break
                end += 1
            if nfa_right:
                stack.append(nfa_right)
            chars = regex[start:end]
            nfa_right = parse_regex(chars)
            i = end

        # Syntactic sugar
        elif regex[i] == '[':
            start = i + 1
            end = start
            count_open_parentheses = 1
            while end < len(regex):
                if regex[end] == '[':
                    count_open_parentheses += 1
                elif regex[end] == ']':
                    count_open_parentheses -= 1
                    if count_open_parentheses == 0:
                        break
                end += 1
            if nfa_right:
                stack.append(nfa_right)
            nfa_right = Sugar(regex[start:end])
            i = end

        else:
            if regex[i] == '\\':
                i += 1
            if nfa_right:
                stack.append(nfa_right)
            nfa_right = Char(regex[i])
        i += 1

    # Concat
    while stack:
        if nfa_right:
            nfa_right = Concat(stack.pop(), nfa_right)
        else:
            nfa_right = stack.pop()

    # Union
    nfa_right = Union(nfa_left, nfa_right)

    return nfa_right
