"""Integration tests running example programs."""
import pytest
from pathlib import Path
from turing_machine import Machine


EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


class TestBinaryIncrement:
    """Test binary_increment.mt example."""

    def test_increment_single_digit(self):
        """Test incrementing single binary digit."""
        progtext = (EXAMPLES_DIR / "binary_increment.mt").read_text()
        machine = Machine(progtext, tape="0")
        for _ in machine:
            pass
        assert str(machine.tape) == "1"

    def test_increment_multi_digit(self):
        """Test incrementing multi-digit binary number."""
        progtext = (EXAMPLES_DIR / "binary_increment.mt").read_text()
        machine = Machine(progtext, tape="1011")
        for _ in machine:
            pass
        assert str(machine.tape) == "1100"

    def test_increment_all_ones(self):
        """Test incrementing all ones (overflow)."""
        progtext = (EXAMPLES_DIR / "binary_increment.mt").read_text()
        machine = Machine(progtext, tape="111")
        for _ in machine:
            pass
        assert str(machine.tape) == "1000"

    def test_increment_zero(self):
        """Test incrementing zero."""
        progtext = (EXAMPLES_DIR / "binary_increment.mt").read_text()
        machine = Machine(progtext, tape="0")
        for _ in machine:
            pass
        assert str(machine.tape) == "1"

    def test_increment_various_inputs(self):
        """Test incrementing various binary numbers."""
        progtext = (EXAMPLES_DIR / "binary_increment.mt").read_text()
        test_cases = [
            ("1", "10"),
            ("10", "11"),
            ("11", "100"),
            ("101", "110"),
            ("1001", "1010"),
        ]
        for input_val, expected in test_cases:
            machine = Machine(progtext, tape=input_val)
            for _ in machine:
                pass
            assert str(machine.tape) == expected


class TestInvertBits:
    """Test invert_bits.mt example."""

    def test_invert_simple(self):
        """Test simple bit inversion."""
        progtext = (EXAMPLES_DIR / "invert_bits.mt").read_text()
        machine = Machine(progtext, tape="1010")
        for _ in machine:
            pass
        assert str(machine.tape) == "0101"

    def test_invert_all_zeros(self):
        """Test inverting all zeros."""
        progtext = (EXAMPLES_DIR / "invert_bits.mt").read_text()
        machine = Machine(progtext, tape="000")
        for _ in machine:
            pass
        assert str(machine.tape) == "111"

    def test_invert_all_ones(self):
        """Test inverting all ones."""
        progtext = (EXAMPLES_DIR / "invert_bits.mt").read_text()
        machine = Machine(progtext, tape="111")
        for _ in machine:
            pass
        assert str(machine.tape) == "000"

    def test_invert_single_bit(self):
        """Test inverting single bit."""
        progtext = (EXAMPLES_DIR / "invert_bits.mt").read_text()
        machine = Machine(progtext, tape="0")
        for _ in machine:
            pass
        assert str(machine.tape) == "1"
        machine = Machine(progtext, tape="1")
        for _ in machine:
            pass
        assert str(machine.tape) == "0"


class TestUnaryAddition:
    """Test unary_addition.mt example."""

    def test_add_simple(self):
        """Test simple unary addition."""
        progtext = (EXAMPLES_DIR / "unary_addition.mt").read_text()
        machine = Machine(progtext, tape="||+||")
        for _ in machine:
            pass
        result = str(machine.tape)
        assert result.count("|") == 4

    def test_add_one_plus_one(self):
        """Test 1 + 1 in unary."""
        progtext = (EXAMPLES_DIR / "unary_addition.mt").read_text()
        machine = Machine(progtext, tape="|+|")
        for _ in machine:
            pass
        result = str(machine.tape)
        assert result == "||"

    def test_add_three_plus_two(self):
        """Test 3 + 2 in unary."""
        progtext = (EXAMPLES_DIR / "unary_addition.mt").read_text()
        machine = Machine(progtext, tape="|||+||")
        for _ in machine:
            pass
        result = str(machine.tape)
        assert result == "|||||"

    def test_add_zero_plus_n(self):
        """Test 0 + n in unary (empty first part)."""
        progtext = (EXAMPLES_DIR / "unary_addition.mt").read_text()
        machine = Machine(progtext, tape="+||")
        for _ in machine:
            pass
        result = str(machine.tape)
        assert result == "||"


class TestEraseProgram:
    """Test erase.mt example."""

    def test_erase_simple(self):
        """Test erasing a simple word."""
        progtext = (EXAMPLES_DIR / "erase.mt").read_text()
        machine = Machine(progtext, tape="abc")
        with pytest.raises(SyntaxError):
            for _ in machine:
                pass
        result = str(machine.tape)
        assert result == "_"

    def test_erase_single_char(self):
        """Test erasing single character."""
        progtext = (EXAMPLES_DIR / "erase.mt").read_text()
        machine = Machine(progtext, tape="a")
        with pytest.raises(SyntaxError):
            for _ in machine:
                pass
        result = str(machine.tape)
        # Tape should be empty after erase
        assert result == "_"


class TestExecutionStepCount:
    """Test that programs terminate in reasonable time."""

    def test_binary_increment_step_count(self):
        """Test binary increment completes in reasonable steps."""
        progtext = (EXAMPLES_DIR / "binary_increment.mt").read_text()
        machine = Machine(progtext, tape="1111")
        steps = 0
        for _ in machine:
            steps += 1
        assert steps < 100  # Should complete quickly

    def test_invert_bits_step_count(self):
        """Test invert bits completes in reasonable steps."""
        progtext = (EXAMPLES_DIR / "invert_bits.mt").read_text()
        machine = Machine(progtext, tape="10101010")
        steps = 0
        for _ in machine:
            steps += 1
        assert steps < 50

    def test_unary_addition_step_count(self):
        """Test unary addition completes in reasonable steps."""
        progtext = (EXAMPLES_DIR / "unary_addition.mt").read_text()
        machine = Machine(progtext, tape="|||+|||")
        steps = 0
        for _ in machine:
            steps += 1
        assert steps < 100
