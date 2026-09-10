"""Unit tests for Tape class."""
import pytest
from turing_machine import Tape


class TestTapeBasics:
    """Test basic tape functionality."""

    def test_empty_tape(self):
        """Test creating an empty tape."""
        tape = Tape()
        assert str(tape.content) == ""
        assert ~tape == "_"
        assert tape.current == 0

    def test_tape_with_content(self):
        """Test tape with initial content."""
        tape = Tape("hello")
        assert tape[0] == "h"
        assert tape[4] == "o"
        assert tape[5] == "_"

    def test_custom_null_character(self):
        """Test tape with custom null character."""
        tape = Tape("abc", null="#")
        assert tape[3] == "#"
        assert tape[-1] == "#"

    def test_tape_length(self):
        """Test tape length."""
        tape = Tape("test")
        assert len(tape) == 4
        assert len(Tape()) == 0


class TestTapeMovement:
    """Test tape head movement."""

    def test_move_right(self):
        """Test moving head right."""
        tape = Tape("abc")
        assert ~tape == "a"
        +tape
        assert ~tape == "b"
        +tape
        assert ~tape == "c"

    def test_move_left(self):
        """Test moving head left."""
        tape = Tape("abc")
        tape.current = 2
        assert ~tape == "c"
        -tape
        assert ~tape == "b"
        -tape
        assert ~tape == "a"

    def test_move_beyond_boundaries(self):
        """Test moving beyond tape boundaries."""
        tape = Tape("abc")
        +tape
        +tape
        +tape
        assert ~tape == "_"
        -tape
        -tape
        -tape
        -tape
        assert ~tape == "_"


class TestTapeWriting:
    """Test writing to tape."""

    def test_write_in_bounds(self):
        """Test writing within tape bounds."""
        tape = Tape("abc")
        tape @= "x"
        assert tape[0] == "x"
        assert tape.content == "xbc"

    def test_write_with_movement(self):
        """Test writing after movement."""
        tape = Tape("abc")
        +tape
        tape @= "y"
        assert tape[1] == "y"
        assert tape.content == "ayc"

    def test_write_null_in_bounds(self):
        """Test writing null character in bounds normalizes tape."""
        tape = Tape("abc")
        +tape
        +tape
        tape @= "_"
        # Content is normalized after writing
        assert "_" not in tape.content
        assert len(tape) == 2

    def test_write_beyond_right(self):
        """Test writing beyond right boundary extends tape."""
        tape = Tape("ab")
        tape.current = 5
        tape @= "x"
        assert tape[5] == "x"

    def test_write_beyond_left(self):
        """Test writing beyond left boundary extends tape."""
        tape = Tape("abc")
        -tape
        -tape
        -tape
        tape @= "z"
        assert ~tape == "z"


class TestTapeNormalization:
    """Test tape normalization."""

    def test_normalization_removes_trailing_nulls(self):
        """Test normalization removes trailing nulls."""
        tape = Tape("abc")
        tape.current = 5
        tape @= "_"
        # After normalization, tape adjusts
        assert tape.content == "abc"

    def test_normalization_adjusts_position(self):
        """Test normalization adjusts head position."""
        tape = Tape("test")
        initial_pos = tape.current
        tape._normalize()
        assert tape.current == initial_pos


class TestTapeRepresentation:
    """Test tape string representation."""

    def test_tape_str(self):
        """Test tape string representation."""
        tape = Tape("hello")
        result = str(tape)
        assert "h" in result
        assert "o" in result

    def test_tape_mark(self):
        """Test tape mark shows head position."""
        tape = Tape("abc")
        tape.current = 1
        mark = tape.mark
        assert "^" in mark


class TestTapeEdgeCases:
    """Test edge cases for tape."""

    def test_single_character_tape(self):
        """Test single character tape."""
        tape = Tape("x")
        assert tape[0] == "x"
        assert tape[1] == "_"

    def test_write_same_character(self):
        """Test writing same character."""
        tape = Tape("aaa")
        tape @= "a"
        assert tape[0] == "a"
        assert len(tape) == 3

    def test_large_movement(self):
        """Test large head movements."""
        tape = Tape("x")
        for _ in range(100):
            +tape
        assert tape.current == 100
        assert ~tape == "_"
