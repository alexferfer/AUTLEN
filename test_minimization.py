"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automaton import FiniteAutomaton
from utils import AutomataFormat, deterministic_automata_isomorphism


class TestMinimize(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_minimize(self, automaton, simplified):
        """Test that the minimized automaton is the simplified one."""
        minimized = automaton.to_minimized()
        equiv_map = deterministic_automata_isomorphism(minimized, simplified)

        self.assertTrue(equiv_map is not None)

    def test_empty_language(self):
        """Test an automaton for the empty language."""
        automaton_str = """
        Automaton:
            Symbols: a

            Initial
            NotReached1
            NotReached2
            Empty

            ini Initial -a-> Empty
            NotReached1 -a-> NotReached2
            NotReached2 -a-> Empty
            Empty -a-> Empty
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: a

            Initial

            ini Initial -a-> Initial
        """

        simplified = AutomataFormat.read(simplified_str)

        self._check_minimize(automaton, simplified)

    def test_empty_str_language(self):
        """Test an automaton for the empty language."""
        automaton_str = """
        Automaton:
            Symbols: a

            Initial final
            NotReached1
            NotReached2
            Empty

            ini Initial -a-> Empty
            NotReached1 -a-> NotReached2
            NotReached2 -a-> Empty
            Empty -a-> Empty
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: a

            Initial final
            Empty 

            ini Initial -a-> Empty
            Empty -a-> Empty
        """

        simplified = AutomataFormat.read(simplified_str)

        self._check_minimize(automaton, simplified)

    def test_redundant_states(self):
        """Test an automaton for the empty language."""
        automaton_str = """
        Automaton:
            Symbols: ab

            Initial
            B1 final
            B2 final
            Empty

            ini Initial -a-> B1
            Initial -b-> Empty
            B1 -a-> B1
            B1 -b-> B2
            B2 -a-> B1
            B2 -b-> B1
            Empty -a-> Empty
            Empty -b-> Empty
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: ab

            Initial
            B final
            Empty

            ini Initial -a-> B
            Initial -b-> Empty
            B -a-> B
            B -b-> B
            Empty -a-> Empty
            Empty -b-> Empty
        """

        simplified = AutomataFormat.read(simplified_str).to_deterministic()

        self._check_minimize(automaton, simplified)

    def test_all_final_and_unreachable(self):
        """Todos los estados alcanzables son finales con estado inaccesible."""
        automaton_str = """
        Automaton:
            Symbols: ab

            q0 final
            q1 final
            unreach

            ini q0 -a-> q1
            q0 -b-> q0
            q1 -a-> q0
            q1 -b-> q1
            unreach -a-> q0
            unreach -b-> q1
        """
        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: ab

            q0 final

            ini q0 -a-> q0
            q0 -b-> q0
        """
        simplified = AutomataFormat.read(simplified_str)
        self._check_minimize(automaton, simplified)

    def test_periodic_equivalent_states(self):
        """Reducción de 4 estados a 2 para cadenas de longitud par."""
        automaton_str = """
        Automaton:
            Symbols: a

            q0 final
            q1
            q2 final
            q3

            ini q0 -a-> q1
            q1 -a-> q2
            q2 -a-> q3
            q3 -a-> q0
        """
        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: a

            even final
            odd

            ini even -a-> odd
            odd -a-> even
        """
        simplified = AutomataFormat.read(simplified_str)
        self._check_minimize(automaton, simplified)

if __name__ == '__main__':
    unittest.main()
