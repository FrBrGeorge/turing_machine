# Turing Machine Emulator

A simple, pure Python command-line Turing Machine tabular interpreter. This project implements a Turing machine that can execute programs defined in tabular format.

## Features

- **Tabular program format**: Define Turing machines using an intuitive table-based syntax
- **Command-line interface**: Easy-to-use CLI for running Turing machine programs
- **Step-by-step debugging**: Built-in debug mode for tracing execution
- **Configurable tape**: Support for custom symbols, null characters, and separators
- **Execution limits**: Prevents infinite loops with configurable step limits

## Installation

### Requirements

- Python 3.12 or higher

### From source

```bash
git clone https://github.com/FrBrGeorge/turing_machine.git
cd turing_machine
pip install -e .
```

## Usage

### Command Line

```bash
turing-machine <program_file> [--input <word>] [options]
```

#### Arguments

- `program` (required): Path to the Turing machine program file

#### Options

- `--input, -i <word>`: Input word to process (if not provided, reads from stdin)
- `--debug, -d`: Enable step-by-step debugging mode
- `--verbose, -v`: Increase verbosity (can be used multiple times: `-v` or `-vv`)
- `--help, -h`: Show help message

#### Examples

```bash
# Run with input from command line
turing-machine examples/binary_increment.mt --input "1011"

# Run with input from stdin
echo "1011" | turing-machine examples/binary_increment.mt

# Debug mode
turing-machine examples/binary_increment.mt --input "1011" --debug

# Verbose output
turing-machine examples/binary_increment.mt --input "1011" -vv
```

### Program Format

Turing machine programs are defined in a tabular format:

```
<alphabet>
<state> <rule_1> <rule_2> ... <rule_n>
...
```

#### Alphabet Line

The first line defines the symbols in the alphabet, separated by spaces:

```
_ 0 1
```

This defines a 3-symbol alphabet: `_` (null/blank), `0`, and `1`.

#### State Lines

Each subsequent line defines transitions for a state. The format is:

- First column: state name
- Following columns: rules for each symbol in the alphabet order

Each rule has the format: `symbol,direction,next_state`

- `symbol`: Character to write (empty means no change)
- `direction`: `L` (left), `R` (right), or `N` (no move)
- `next_state`: Next state (empty means stay in current state)

Empty rules are denoted by `,,` (two commas).

#### Comments

Lines starting with `#` are treated as comments.

### Example Programs

#### Binary Increment

Adds 1 to a binary number.

```
 _ 0 1
0 ,L,1 ,R, ,R,
1 1,R,! 1,N,! 0,L,
```

Input: `1011` → Output: `1100`

#### Delete 'a' from String

Removes all 'a' characters from an input string containing 'a', 'b', 'c'.

```
       a      b     c      _      #
0    ,R,    ,R,   ,R,   #,L,1
1    ,L,    ,L,   ,L,    ,R,2   ,L,
2   _,R,   _,R,3 _,R,4   ,R,!  _,R,!
3    ,R,    ,R,   ,R,   b,L,1   ,R,
4    ,R,    ,R,   ,R,   c,L,1   ,R,
```

Input: `aabaca` → Output: `bca`

## API Reference

### Tape

Represents the Turing machine tape with infinite blank cells.

```python
from turing_machine import Tape

tape = Tape("hello")
```

**Attributes:**
- `content`: Current non-null content of the tape
- `current`: Current head position
- `null`: Blank symbol (default: `_`)

**Methods:**
- `tape[idx]`: Get symbol at position `idx` (returns null if out of bounds)
- `~tape`: Get current symbol under head
- `+tape`: Move head right
- `-tape`: Move head left
- `tape @= symbol`: Write symbol at current position
- `str(tape)`: Get tape representation with head marked

### Prog

Represents a Turing machine program.

```python
from turing_machine import Prog

prog = Prog(progtext, null="_", sep=",")
```

**Attributes:**
- `alphabet`: List of symbols
- `states`: List of state names
- `sep`: Separator character (default: `,`)
- `null`: Null symbol (default: `_`)

**Methods:**
- `prog[state, symbol]`: Get rule for state-symbol pair (returns `[symbol, direction, next_state]`)
- `str(prog)`: Get formatted program table

### Machine

The main Turing machine executor.

```python
from turing_machine import Machine

machine = Machine(progtext, tape="input_word", limit=32768)

for state, symbol in machine:
    print(f"State: {state}, Symbol: {symbol}")

result = str(machine.tape)
```

**Attributes:**
- `prog`: The program (Prog object)
- `tape`: The tape (Tape object)
- `state`: Current state
- `limit`: Maximum execution steps (default: 32768)

**Methods:**
- Iteration: Yields `(state, symbol)` at each step
- `bool(machine)`: Returns True if final word is valid (no nulls in content, head points to non-null)

## Architecture

The project consists of three main classes:

1. **Tape**: Manages the infinite tape with current head position
   - Handles writing and reading symbols
   - Normalizes content to remove leading/trailing nulls
   - Provides string representation for visualization

2. **Prog**: Parses and stores the Turing machine program
   - Reads tabular format
   - Stores transitions as a dictionary
   - Manages alphabet and states

3. **Machine**: Orchestrates tape and program execution
   - Iterates through execution steps
   - Applies transitions from the program
   - Enforces execution limits to prevent infinite loops

## Technical Details

### Tape Representation

The tape is infinite in both directions. The implementation:
- Stores only the non-null portion of the content
- Normalizes after each write operation
- Returns the null character for positions outside the content range

### Execution Model

At each step:
1. Read the symbol under the head
2. Look up the transition rule for (state, symbol)
3. Write the new symbol (if specified)
4. Move the head (L/R/N)
5. Change state (if specified)
6. Continue until reaching a stop state or limit

### Stop Conditions

Execution stops when:
- The machine reaches state `!` (halt state)
- The execution limit is reached (raises RuntimeError)
- An invalid rule is encountered (raises RuntimeError)

## Examples

All example programs are in the `examples/` directory:

- `binary_increment.mt` - Binary number increment
- `del_a.mt` - Delete character 'a' from string
- `double.mt` - Double a unary number
- `erase.mt` - Erase tape
- `ex.mt` - Complex example
- `invert_bits.mt` - Invert binary digits
- `unary_addition.mt` - Add two unary numbers

Try them:

```bash
turing-machine examples/binary_increment.mt --input "101"
turing-machine examples/unary_addition.mt --input "xx+yyy"
```

## Debugging

Use the `--debug` or `-d` flag to enter step-by-step execution mode:

```bash
turing-machine examples/binary_increment.mt --input "1011" --debug
```

In debug mode, after each step you can:
- Press Enter to continue
- Type `?` to see the program table
- Type `q` to quit

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Tests include:
- Unit tests for Tape, Prog, and Machine classes
- Integration tests with example programs
- Predefined input/output validation

## License

MIT - See LICENSE file for details

## Author

Fr. Br. George (frbrgeorge@gmail.com)

## References

- [Turing Machine Syntax and Examples](https://cmcmsu.info/1course/alg.schema.mt.htm)
