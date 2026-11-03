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
        clausura_inicial = self._lambda_closure({self.initial_state})
        estados_afd = [clausura_inicial]

        afd = FiniteAutomaton("q0", set(), set(self.symbols), {}, set())

        i = 0
        while i < len(estados_afd):
            conjunto_actual = estados_afd[i]
            nombre_origen = f"q{i}"
            afd.states.add(nombre_origen)

            if conjunto_actual.intersection(self.final_states):
                afd.final_states.add(nombre_origen)

            for symbol in self.symbols:
                destinos = set()
                for estado in conjunto_actual:
                    destinos_simbolo = self.transitions.get(estado, {}).get(symbol, set())
                    destinos.update(destinos_simbolo)

                clausura_destino = self._lambda_closure(destinos)

                if clausura_destino not in estados_afd:
                    estados_afd.append(clausura_destino)

                indice_destino = estados_afd.index(clausura_destino)
                nombre_destino = f"q{indice_destino}"
                afd.add_transition(nombre_origen, symbol, nombre_destino)

            i += 1

        return afd

    def to_minimized(self):
        afd = self.to_deterministic()

        finales = set(afd.final_states)
        no_finales = afd.states - finales

        particion = []
        if no_finales:
            particion.append(no_finales)
        if finales:
            particion.append(finales)

        cambio = True
        while cambio:
            cambio = False
            nueva_particion = []

            for grupo in particion:
                subgrupos = []
                for estado in grupo:
                    colocado = False
                    for sub in subgrupos:
                        representante = next(iter(sub))
                        equivalentes = True

                        for symbol in afd.symbols:
                            dest1 = next(iter(afd.transitions[estado][symbol]))
                            dest2 = next(iter(afd.transitions[representante][symbol]))

                            for g in particion:
                                if (dest1 in g) != (dest2 in g):
                                    equivalentes = False
                                    break
                            if not equivalentes:
                                break

                        if equivalentes:
                            sub.add(estado)
                            colocado = True
                            break

                    if not colocado:
                        subgrupos.append({estado})

                nueva_particion.extend(subgrupos)
                if len(subgrupos) > 1:
                    cambio = True

            particion = nueva_particion

        estado_inicial_min = None
        for i in range(len(particion)):
            if afd.initial_state in particion[i]:
                estado_inicial_min = f"q{i}"
                break

        aut_min = FiniteAutomaton(estado_inicial_min, set(), set(afd.symbols), {}, set())

        for i in range(len(particion)):
            grupo = particion[i]
            nombre_origen = f"q{i}"
            aut_min.states.add(nombre_origen)

            if grupo.intersection(afd.final_states):
                aut_min.final_states.add(nombre_origen)

            representante = next(iter(grupo))
            for symbol in afd.symbols:
                dest = next(iter(afd.transitions[representante][symbol]))
                for j in range(len(particion)):
                    if dest in particion[j]:
                        aut_min.add_transition(nombre_origen, symbol, f"q{j}")
                        break

        return aut_min

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
