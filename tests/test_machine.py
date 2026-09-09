"""Unit tests for Machine class."""
import pytest
from turing_machine import Machine, Tape


class TestMachineInitialization:
    """Test machine initialization."""

    def test_create_machine(self):
        """Test creating a machine."""
        progtext = "_ a\n0 ,R, ,L,"
        machine = Machine(progtext)
        assert machine.state == "0"
        assert machine.stop == "!"

    def test_machine_with_input(self):
        """Test machine with input word."""
        progtext = "_ a\n0 ,R, ,L,"
        machine = Machine(progtext, tape="hello")
        assert machine.tape.content == "hello"

    def test_machine_with_custom_limit(self):
        """Test machine with custom execution limit."""
        progtext = "_ a\n0 ,R, ,L,"
        machine = Machine(progtext, limit=1000)
        assert machine.limit == 1000

    def test_machine_with_custom_stop_state(self):
        """Test machine with custom stop state."""
        progtext = "_ a\n0 ,R, ,L,"
        machine = Machine(progtext, stop="halt")
        assert machine.stop == "halt"


class TestMachineExecution:
    """Test machine execution."""

    def test_simple_execution(self):
        """Test simple machine execution."""
        progtext = "_ a\n0 ,R,! ,L,"
        machine = Machine(progtext, tape="a")
        states = []
        for state, symbol in machine:
            states.append(state)
        assert "0" in states
        assert machine.state == "!"

    def test_multiple_steps(self):
        """Test execution with multiple steps."""
        progtext = "_ a\n0 ,R,0 ,R,!\n1 ,L,!"
        machine = Machine(progtext, tape="aa")
        steps = 0
        for state, symbol in machine:
            steps += 1
        assert steps > 1

    def test_tape_modification(self):
        """Test that tape is modified during execution."""
        progtext = "_ a\n0 b,R,!"
        machine = Machine(progtext, tape="a")
        for _ in machine:
            pass
        assert machine.tape[0] == "b"


class TestMachineExamples:
    """Test machine with real example programs."""

    def test_invert_bits(self):
        """Test invert_bits program."""
        progtext = """ _ 0 1
        0 ,L,! 1,R, 0,R,
        """
        machine = Machine(progtext, tape="1010")
        for _ in machine:
            pass
        result = str(machine.tape)
        assert result == "0101"

    def test_binary_increment(self):
        """Test binary_increment program."""
        progtext = """ _ 0 1
        0 ,L,1 ,R, ,R,
        1 1,R,! 1,N,! 0,L,
        """
        machine = Machine(progtext, tape="101")
        for _ in machine:
            pass
        result = str(machine.tape)
        assert result == "110"

    def test_binary_increment_overflow(self):
        """Test binary_increment with all 1s."""
        progtext = """ _ 0 1
        0 ,L,1 ,R, ,R,
        1 1,R,! 1,N,! 0,L,
        """
        machine = Machine(progtext, tape="111")
        for _ in machine:
            pass
        result = str(machine.tape)
        assert result == "1000"

    def test_unary_addition(self):
        """Test unary_addition program."""
        progtext = """    _     |     +
        0  ,,   ,R,  |,R,1
        1 ,L,2  ,R,   ,,
        2  ,,  _,L,!  ,,
        """
        machine = Machine(progtext, tape="||+||", null="_", sep=",")
        for _ in machine:
            pass
        result = str(machine.tape)
        # Should have 4 pipes (2 + 2)
        assert result == "||||"


class TestMachineValidation:
    """Test machine validation and error handling."""

    def test_machine_bool_valid_output(self):
        """Test machine validation with valid output."""
        progtext = "_ a\n0 b,R,!"
        machine = Machine(progtext, tape="a")
        for _ in machine:
            pass
        assert bool(machine) is True

    def test_machine_bool_null_in_output(self):
        """Test machine validation fails with null in output."""
        progtext = "_ a\n0 _,R,!"
        machine = Machine(progtext, tape="a")
        for _ in machine:
            pass
        assert bool(machine) is False

    def test_execution_limit_exceeded(self):
        """Test that execution limit is enforced."""
        # Infinite loop program
        progtext = "_ a\n0 ,R,0"
        machine = Machine(progtext, tape="a", limit=10)
        with pytest.raises(RuntimeError, match="Limit of 10 steps is reached"):
            for _ in machine:
                pass

    def test_invalid_move_direction(self):
        """Test error on invalid move direction."""
        progtext = "_ a\n0 ,X,!"
        machine = Machine(progtext, tape="a")
        with pytest.raises(RuntimeError, match="Incorrect rule"):
            for _ in machine:
                pass


class TestMachineIteration:
    """Test machine iteration behavior."""

    def test_iteration_yields_state_symbol(self):
        """Test that iteration yields (state, symbol) tuples."""
        progtext = "_ a\n0 ,R,!"
        machine = Machine(progtext, tape="a")
        for state, symbol in machine:
            assert isinstance(state, str)
            assert isinstance(symbol, str)

    def test_stops_at_stop_state(self):
        """Test that iteration stops at stop state."""
        progtext = "_ a\n0 ,R,1\n1 ,R,!"
        machine = Machine(progtext, tape="aa")
        final_state = None
        for state, symbol in machine:
            final_state = state
        assert final_state == "!"

    def test_state_progression(self):
        """Test state changes during execution."""
        progtext = "_ a\n0 ,R,1\n1 ,R,2\n2 ,R,!"
        machine = Machine(progtext, tape="aaa")
        states_seen = set()
        for state, symbol in machine:
            states_seen.add(state)
        assert "0" in states_seen
        assert "1" in states_seen
        assert "2" in states_seen
        assert "!" in states_seen
