"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automaton import FiniteAutomaton
from utils import AutomataFormat, deterministic_automata_isomorphism


class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(self, automaton, expected):
        """Test that the transformed automaton is as the expected one."""

        automaton.draw(filename="automaton", view=False)

        transformed = automaton.to_deterministic()

        transformed.draw(filename="transformed", view=False)
        expected.draw(filename="expected", view=False)

        equiv_map = deterministic_automata_isomorphism(expected, transformed)

        self.assertTrue(equiv_map is not None)

    def test_case1(self):
        """Test Case 1."""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        q0
        qf final
        
        ini q0 -0-> qf
        qf -1-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        q0
        qf final
        empty
        
        ini q0 -0-> qf
        q0 -1-> empty
        qf -0-> empty
        qf -1-> qf
        empty -0-> empty
        empty -1-> empty
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_lambda_and_nondeterminism(self):
        """AFnD con transiciones lambda y estado sumidero."""
        automaton_str = """
        Automaton:
            Symbols: ab

            q0
            q1
            q2 final

            ini q0 --> q1
            q0 -a-> q1
            q1 -b-> q2
            q2 -a-> q2
            q2 -b-> q2
        """
        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: ab

            q01
            q1
            q2 final
            empty

            ini q01 -a-> q1
            q01 -b-> q2
            q1 -a-> empty
            q1 -b-> q2
            q2 -a-> q2
            q2 -b-> q2
            empty -a-> empty
            empty -b-> empty
        """
        expected = AutomataFormat.read(expected_str)
        self._check_transform(automaton, expected)

    def test_multiple_transitions_same_symbol(self):
        """AFnD que reconoce cadenas terminadas en '01'."""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q2 final

            ini q0 -0-> q0
            q0 -1-> q0
            q0 -0-> q1
            q1 -1-> q2
        """
        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: 01

            s0
            s1
            s2 final

            ini s0 -0-> s1
            s0 -1-> s0
            s1 -0-> s1
            s1 -1-> s2
            s2 -0-> s1
            s2 -1-> s0
        """
        expected = AutomataFormat.read(expected_str)
        self._check_transform(automaton, expected)


if __name__ == '__main__':
    unittest.main()
