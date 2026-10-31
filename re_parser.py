"""
    Equipo docente de Autómatas y Lenguajes Curso 2025-26
    Última modificación: 18 de septiembre de 2025
"""

from automaton import FiniteAutomaton


def _re_to_rpn(re_string):
    """
    Convert re to reverse polish notation (RPN).

    Does not check that the input re is syntactically correct.

    Args:
        re_string: Regular expression in infix notation. Type: str

    Returns:
        Regular expression in reverse polish notation. Type: str

    """
    stack = []  # List of strings
    rpn_string = ""
    for x in re_string:
        if x == "+":
            while len(stack) > 0 and stack[-1] != "(":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == ".":
            while len(stack) > 0 and stack[-1] == ".":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == "(":
            stack.append(x)
        elif x == ")":
            while stack[-1] != "(":
                rpn_string += stack.pop()
            stack.pop()
        else:
            rpn_string += x

    while len(stack) > 0:
        rpn_string += stack.pop()

    return rpn_string


class REParser():

    def __init__(self) -> None:
        self.state_counter = 0

    def _get_new_state(self):
        state = f"q{self.state_counter}"
        self.state_counter += 1
        return state

    def _create_automaton_empty(self):
        q_ini = self._get_new_state()
        q_fin = self._get_new_state()
        return FiniteAutomaton(
            initial_state=q_ini,
            states={q_ini, q_fin},
            symbols=set(),
            transitions={q_ini: {}, q_fin: {}},
            final_states={q_fin}
        )

    def _create_automaton_lambda(self):
        q_ini = self._get_new_state()
        q_fin = self._get_new_state()
        aut = FiniteAutomaton(
            initial_state=q_ini,
            states={q_ini, q_fin},
            symbols=set(),
            transitions={},
            final_states={q_fin}
        )
        aut.add_transition(q_ini, None, q_fin)
        return aut

    def _create_automaton_symbol(self, symbol):
        q_ini = self._get_new_state()
        q_fin = self._get_new_state()
        aut = FiniteAutomaton(
            initial_state=q_ini,
            states={q_ini, q_fin},
            symbols={symbol},
            transitions={},
            final_states={q_fin}
        )
        aut.add_transition(q_ini, symbol, q_fin)
        return aut

    def _create_automaton_concat(self, automaton1, automaton2):
        final_a1 = next(iter(automaton1.final_states))

        new_states = set(automaton1.states).union(automaton2.states)
        new_symbols = set(automaton1.symbols).union(automaton2.symbols)

        new_transitions = {}
        for aut in (automaton1, automaton2):
            for src, sym_map in aut.transitions.items():
                if src not in new_transitions:
                    new_transitions[src] = {}
                for sym, targets in sym_map.items():
                    if sym not in new_transitions[src]:
                        new_transitions[src][sym] = set()
                    new_transitions[src][sym].update(targets)

        if final_a1 not in new_transitions:
            new_transitions[final_a1] = {}
        if None not in new_transitions[final_a1]:
            new_transitions[final_a1][None] = set()
        new_transitions[final_a1][None].add(automaton2.initial_state)

        return FiniteAutomaton(
            initial_state=automaton1.initial_state,
            states=new_states,
            symbols=new_symbols,
            transitions=new_transitions,
            final_states=set(automaton2.final_states)
        )

    def _create_automaton_union(self, automaton1, automaton2):
        q_ini = self._get_new_state()
        q_fin = self._get_new_state()

        final_a1 = next(iter(automaton1.final_states))
        final_a2 = next(iter(automaton2.final_states))

        new_states = {q_ini, q_fin}.union(automaton1.states).union(automaton2.states)
        new_symbols = set(automaton1.symbols).union(automaton2.symbols)

        new_transitions = {}
        for aut in (automaton1, automaton2):
            for src, sym_map in aut.transitions.items():
                if src not in new_transitions:
                    new_transitions[src] = {}
                for sym, targets in sym_map.items():
                    if sym not in new_transitions[src]:
                        new_transitions[src][sym] = set()
                    new_transitions[src][sym].update(targets)

        new_transitions[q_ini] = {None: {automaton1.initial_state, automaton2.initial_state}}

        for f in (final_a1, final_a2):
            if f not in new_transitions:
                new_transitions[f] = {}
            if None not in new_transitions[f]:
                new_transitions[f][None] = set()
            new_transitions[f][None].add(q_fin)

        return FiniteAutomaton(
            initial_state=q_ini,
            states=new_states,
            symbols=new_symbols,
            transitions=new_transitions,
            final_states={q_fin}
        )

    def _create_automaton_star(self, automaton):
        q_ini = self._get_new_state()
        q_fin = self._get_new_state()

        final_a = next(iter(automaton.final_states))

        new_states = {q_ini, q_fin}.union(automaton.states)
        new_symbols = set(automaton.symbols)

        new_transitions = {}
        for src, sym_map in automaton.transitions.items():
            if src not in new_transitions:
                new_transitions[src] = {}
            for sym, targets in sym_map.items():
                if sym not in new_transitions[src]:
                    new_transitions[src][sym] = set()
                new_transitions[src][sym].update(targets)

        new_transitions[q_ini] = {None: {automaton.initial_state, q_fin}}

        if final_a not in new_transitions:
            new_transitions[final_a] = {}
        if None not in new_transitions[final_a]:
            new_transitions[final_a][None] = set()
        new_transitions[final_a][None].update({q_fin, automaton.initial_state})

        return FiniteAutomaton(
            initial_state=q_ini,
            states=new_states,
            symbols=new_symbols,
            transitions=new_transitions,
            final_states={q_fin}
        )

    def create_automaton(
        self,
        re_string,
    ):
        """
        Create an automaton from a regex.

        Args:
            re_string: String with the regular expression in Kleene notation. Type: str

        Returns:
            Automaton equivalent to the regex. Type: FiniteAutomaton

        """
        if not re_string:
            return self._create_automaton_lambda()

        rpn_string = _re_to_rpn(re_string)

        stack = []  # list of FiniteAutomatons

        self.state_counter = 0
        for x in rpn_string:
            if x == "*":
                aut = stack.pop()
                stack.append(self._create_automaton_star(aut))
            elif x == "+":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_union(aut1, aut2))
            elif x == ".":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_concat(aut1, aut2))
            elif x == "λ":
                stack.append(self._create_automaton_lambda())
            else:
                stack.append(self._create_automaton_symbol(x))

        return stack.pop()
