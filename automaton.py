"""
    Equipo docente de Autómatas y Lenguajes Curso 2025-26
    Última modificación: 18 de septiembre de 2025
"""

from collections import deque
from graphviz import Digraph

"""
    Podéis implementar cualquier función auxiliar que consideréis necesaria
"""


def _get_all_transitions(automaton):
    automaton_all_transitions = []
    for state_ini in automaton.transitions:
        for symbol in automaton.transitions[state_ini]:
            for end_state in automaton.transitions[state_ini][symbol]:
                automaton_all_transitions.append(
                    (state_ini, symbol, end_state))
    return automaton_all_transitions


def is_deterministic(automaton):
    """Check whether an automaton is deterministic."""
    checked = set()

    for start_state, symbol, end_state in _get_all_transitions(automaton):
        if symbol is None:
            return False
        if (start_state, symbol) in checked:
            return False
        checked.add((start_state, symbol))

    return True


class FiniteAutomaton:

    def __init__(self, initial_state, states, symbols, transitions, final_states):
        self.initial_state = initial_state
        self.states = set(states)
        self.symbols = set(symbols)
        self.transitions = transitions if transitions is not None else {}
        self.final_states = set(final_states)

    def add_transition(self, start_state, symbol, end_state):
        self.states.add(start_state)
        self.states.add(end_state)
        if symbol is not None:
            self.symbols.add(symbol)

        if start_state not in self.transitions:
            self.transitions[start_state] = {}
        if symbol not in self.transitions[start_state]:
            self.transitions[start_state][symbol] = set()

        self.transitions[start_state][symbol].add(end_state)

    def _lambda_closure(self, states):
        closure = set(states)
        stack = list(states)

        while stack:
            current = stack.pop()
            lambda_destinations = self.transitions.get(current, {}).get(None, set())
            for dest in lambda_destinations:
                if dest not in closure:
                    closure.add(dest)
                    stack.append(dest)

        return closure

    def accepts(self, cadena):
        current_states = self._lambda_closure({self.initial_state})

        for symbol in cadena:
            next_states = set()
            for state in current_states:
                targets = self.transitions.get(state, {}).get(symbol, set())
                next_states.update(targets)

            current_states = self._lambda_closure(next_states)

            if not current_states:
                return False

        return bool(current_states.intersection(self.final_states))

    def to_deterministic(self):
        pass

    def to_minimized(self):
        pass

    def draw(self, path="./images/", filename="automata.png", view=False):
        dot = Digraph(comment="Automata", format="png")
        dot.attr(rankdir="LR")

        # Nodo invisible para punto inicial
        dot.node("", shape="none")

        # Almacenar estados
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape="doublecircle")
            else:
                dot.node(state, shape="circle")

        # Flecha al estado inicial
        dot.edge("", self.initial_state)

        # Almacenar transiciones
        for state_ini in self.transitions:
            for symbol in self.transitions[state_ini]:
                for state_fin in self.transitions[state_ini][symbol]:
                    dot.edge(state_ini, state_fin,
                             symbol if symbol is not None else "λ")

        dot.render(path+filename, view=view)
