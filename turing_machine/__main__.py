#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys
from . import Machine

HELPURL = "https://cmcmsu.info/1course/alg.schema.mt.htm"

def run(*args):
    parser = argparse.ArgumentParser(description="Turing Machine runner",
                                     epilog=f"See {HELPURL} for synrtax and examples")
    parser.add_argument("program", help="Program in tabular form")
    parser.add_argument("--debug", "-d", action="store_true", help="Step-by-step execution")
    parser.add_argument("--verbose", "-v", default=0, action='count', help="Increase verbosity")
    parser.add_argument("--input", "-i", help="Input word")
    # TODO redefine limit, null, sep etc

    args = parser.parse_args(args or None)
    run.args = args
    progtext = Path(args.program).read_text()
    if not args.input:
        args.input = input()
    mt = Machine(progtext, args.input)
    sw = max(len(str(s)) for s in mt.prog.states)
    for state, symbol in mt:
        info = f"{state:>{sw}}:{symbol}"
        if args.verbose > 1:
            print(f"{' ' * len(info)} {mt.tape}", file=sys.stderr)
            print(f"{info} {mt.tape.mark}", file=sys.stderr)
        elif args.verbose > 0:
            print(mt.tape, file=sys.stderr)
            print(mt.tape.mark, file=sys.stderr)
        if args.debug:
            # TODO cmdline et al.
            while cmd := input(f"{info} -> {mt.prog.get((state, symbol), "UNKNOWN")}> "):
                match cmd:
                    case "?":
                        print(mt.prog)
    if not mt:
        raise SyntaxError(f"Incorrect final word: {mt.tape}")
    return str(mt.tape)

def main():
    try:
        print(run())
    except Exception as E:
        if run.args.debug:
            raise E
        else:
            print("Error:", E, file=sys.stderr)
            exit(1)


if __name__ == "__main__":
    main()
