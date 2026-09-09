#!/usr/bin/env python3
'''
Turing Machine, try 4.
'''
from collections import UserDict
from itertools import groupby

class Band:
    """MT band."""

    def __init__(self, content="", null="_"):
        self.content, self.null = content, null
        self.current = 0

    def __getitem__(self, idx):
        return self[idx] if 0 <= idx < len(self) else self.null

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
            self.content = value + (self.current + 1) * self.null + self.content
        else:
            self.content += (self.current - len(self)) * self.null + value
        self._normalize()

    def _normalize(self):
        while self.content.startswith(self.null):
            self.content = self.content[1:]
            self.current -= 1
        while self.content.endswith(self.null):
            self.content = self.content[:-1]

    def __str__(self):
        return "".join(self[i] for i in range(min(self.current, 0), max(self.current + 1, len(self))))

    def underline(self):
        return "".join("^" if i == self.current else " " for i in range(min(self.current, 0), self.current + 1))


class Prog(UserDict):
    """MT program."""
    alphabet: list[str] = []
    initial: str = "0"
    sep: str = ","
    null: str = "_"

    def __init__(self, progtext, null="_", sep=","):
        self.null, self.sep = null, sep
        self.parse(progtext)

    def parse(self, progtext):
        # TODO AL compatibility mode
        table = [line.strip().split() for line in progtext.split("\n")]
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

    def states(self):
        return [key for key, seq in groupby(self.keys())]

class Machine:
    prog: Prog = None
    band: Band = Band()
    state: str = "0"

    def __init__(self, progtext, band=Band(), null="_", sep=","):
        self.band = Band(band, null)
        self.Prog = Prog(progtext, null, sep)
        self.state = 0
