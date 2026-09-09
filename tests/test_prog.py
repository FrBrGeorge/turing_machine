"""Unit tests for Prog class."""
import pytest
from turing_machine import Prog


class TestProgParsing:
    """Test program parsing."""

    def test_parse_simple_prog(self):
        """Test parsing a simple program."""
        progtext = """
        _ 0 1
        0 ,L,1 ,R, ,R,
        1 1,R,! 1,N,! 0,L,
        """
        prog = Prog(progtext)
        assert prog.alphabet == ["_", "0", "1"]
        assert "0" in prog.states
        assert "1" in prog.states

    def test_parse_with_comments(self):
        """Test parsing with comments."""
        progtext = """
        # This is a comment
        _ a b
        # Another comment
        0 ,R, ,L,
        1 a,N,!
        """
        prog = Prog(progtext)
        assert prog.alphabet == ["_", "a", "b"]
        assert len(prog.states) == 2

    def test_alphabet_extraction(self):
        """Test alphabet is correctly extracted."""
        progtext = "a b c d\n0 ,R, ,L, ,N, ,R,"
        prog = Prog(progtext)
        assert prog.alphabet == ["a", "b", "c", "d"]
        assert len(prog.alphabet) == 4

    def test_invalid_alphabet_length(self):
        """Test error on multi-character symbols."""
        progtext = "ab c\n0 ,R, ,L,"
        with pytest.raises(ValueError, match="Incorrect symbol length"):
            Prog(progtext)


class TestProgRules:
    """Test program rule access."""

    def test_access_rule(self):
        """Test accessing a rule."""
        progtext = "_ a\n0 ,R, ,L,"
        prog = Prog(progtext)
        rule = prog["0", "_"]
        assert rule == ["", "R", ""]

    def test_rule_with_write(self):
        """Test rule with write operation."""
        progtext = "_ a\n0 x,R,1 y,L,2"
        prog = Prog(progtext)
        rule0 = prog["0", "_"]
        assert rule0 == ["x", "R", "1"]
        rule1 = prog["0", "a"]
        assert rule1 == ["y", "L", "2"]

    def test_empty_rules_padding(self):
        """Test that rules are padded with empty rules."""
        progtext = "_ a\n0 ,R,"
        prog = Prog(progtext)
        # Rule for first symbol
        assert prog["0", "_"] == ["", "R", ""]
        # Should have rule for second symbol too (padded)
        assert len(prog["0", "a"]) == 3


class TestProgStates:
    """Test state management."""

    def test_extract_states(self):
        """Test extracting state names."""
        progtext = "_ a\n0 ,R, ,L,\n1 a,R,2\n2 ,L,!"
        prog = Prog(progtext)
        states = prog.states
        assert "0" in states
        assert "1" in states
        assert "2" in states

    def test_state_order(self):
        """Test states are in order of appearance."""
        progtext = "_ a\nq0 ,R, ,L,\nq1 a,R,!\nq2 ,L,!"
        prog = Prog(progtext)
        states = prog.states
        assert states[0] == "q0"
        assert states[1] == "q1"
        assert states[2] == "q2"


class TestProgStringRepresentation:
    """Test program string representation."""

    def test_prog_str(self):
        """Test program string representation."""
        progtext = "_ a\n0 ,R, ,L,\n1 a,N,!"
        prog = Prog(progtext)
        result = str(prog)
        assert "0" in result
        assert "1" in result


class TestProgCustomSeparators:
    """Test custom separator handling."""

    def test_custom_separator(self):
        """Test program with custom separator."""
        progtext = "_ a | 0 ; R ; 1 ; L ;"
        prog = Prog(progtext, sep=";")
        assert prog.alphabet == ["_", "a"]

    def test_custom_null(self):
        """Test program with custom null character."""
        progtext = "# a\n0 ,R, ,L,"
        prog = Prog(progtext, null="#")
        assert prog.null == "#"
