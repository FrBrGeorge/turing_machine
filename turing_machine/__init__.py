#!/usr/bin/env python3
'''
Turing Machine, try 4.
'''
from collections import UserDict
from itertools import groupby

RUNLIMIT = 32768

class Tape:
    """MT tape."""

    def __init__(self, content="", null="_"):
        self.content, self.null = content, null
        self.current = 0

    def __getitem__(self, idx):
        return self.content[idx] if 0 <= idx < len(self) else self.null

    def __invert__(self):
        return self[self.current]

    def __neg__(self):
        self.current -= 1
        return ~self

    def __pos__(self):
        self.current += 1
        return ~self

    def __len__(self):
        return len(self.content)

    def __imatmul__(self, value):
        if 0 <= self.current < len(self):
            self.content = self.content[:self.current] + value + self.content[self.current + 1:]
        elif self.current < 0:
            if value != self.null:
                self.content = value + (self.current + 1) * self.null + self.content
        elif value != self.null:
            self.content += (self.current - len(self)) * self.null + value
        self._normalize()
        return self

    def _normalize(self):
        lcontent = self.content.lstrip(self.null)
        self.current -= len(self) - len(lcontent)
        self.content = self.content.strip(self.null)

    def __str__(self):
        return "".join(self[i] for i in range(min(self.current, 0), max(self.current + 1, len(self))))

    @property
    def mark(self):
        return "".join("^" if i == self.current else " " for i in range(min(self.current, 0), self.current + 1))


class Prog(UserDict):
    """MT program."""
    alphabet: list[str] = []
    initial: str = "0"
    sep: str = ","
    null: str = "_"

    def __init__(self, progtext, null="_", sep=","):
        super().__init__()
        self.null, self.sep = null, sep
        self.parse(progtext)

    def parse(self, progtext):
        # TODO AL compatibility mode
        table = [line.strip().split() for line in progtext.split("\n") if not line.startswith("#")]
        self.alphabet = table[0]
        if any(len(a) != 1 for a in self.alphabet):
            raise ValueError(f"Incorrect symbol length in {table[0]}")
        for i in range(1, len(table)):
            if len(table[i]) == 0:
                continue
            state, *rules = table[i]
            rules += [f"{self.sep * 2}"] * (len(self.alphabet) - len(rules))
            for symbol, textrule in zip(self.alphabet, rules):
                self[state, symbol] = textrule.split(self.sep)

    @property
    def states(self):
        return [key for key, seq in groupby(k for k, _ in self.keys())]

    def __str__(self):
        # TODO mark current state / symbol
        sw = max(len(str(s)) for s in self.states)
        rw = sw + 2 * len(self.sep) + 2 + sw
        result = " " * (sw + 1) + " ".join(f"{a:^{rw}}" for a in self.alphabet)
        for state in self.states:
            rules = [self[state, a] for a in self.alphabet]
            result += f"\n{state:<{sw}} " + " ".join(f"{a + self.sep + m + self.sep + s:^{rw}}" for a, m, s in rules)
        return result

class Machine:
    prog: Prog = None
    tape: Tape = Tape()
    state: str = "0"
    limit: int = RUNLIMIT

    def __init__(self, progtext, tape=Tape(), limit=RUNLIMIT, stop="!", null="_", sep=","):
        self.tape = Tape(tape, null)
        self.prog = Prog(progtext, null, sep)
        self.state, self.stop, self.limit = "0", stop, limit

    def __iter__(self):
        for i in range(self.limit):
            yield self.state, ~self.tape
            if self.state == self.stop:
                break
            symbol, move, state = self.prog[self.state, ~self.tape]
            if move not in "RLN":
                raise RuntimeError(f"Incorrect rule: {self.prog[self.state, ~self.tape]} at {self.state}:{~self.tape}")
            symbol = symbol or ~self.tape
            state = state or self.state
            self.tape @= symbol
            (move == "L" and -self.tape) or (move == "R" and +self.tape)
            self.state = state
        else:
            raise RuntimeError(f"Limit of {self.limit} steps is reached, still running")
        if not self:
            raise SyntaxError(f"Incorrect final word: {self.tape}")

    def __bool__(self):
        """If MT is correct?"""
        return self.tape.null not in self.tape.content and ~self.tape != self.tape.null
