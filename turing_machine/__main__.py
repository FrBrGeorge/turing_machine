#!/usr/bin/env python3
import argparse
import sys
from . import Machine

HELPURL = "https://cmcmsu.info/1course/alg.schema.mt.htm"
RUNLIMIT = 32768

def run(mt, debug, limit=RUNLIMIT):
    sw = max(len(str(s)) for s in mt.prog.states)
    trace = []
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
                    case "q":
                        str(mt.tape)
                    # TODO back
        trace.append((state, mt.tape))
        if len(trace) >= limit:
            raise RuntimeError(f"Limit of {limit} steps is reached, still running")
    return str(mt.tape)

def main(prog, word, debug):
    try:
        print(run(Machine(prog, word), debug))
    except Exception as E:
        if debug:
            raise E
        else:
            print("Error:", E, file=sys.stderr)
            exit(1)

def parseargs(*args):
    parser = argparse.ArgumentParser(description="Turing Machine runner",
                                     epilog=f"See {HELPURL} for syntax and examples")
    parser.add_argument("program", type=argparse.FileType("r"), help="Program in tabular form")
    parser.add_argument("--debug", "-d", action="store_true", help="Step-by-step execution")
    parser.add_argument("--verbose", "-v", default=0, action='count', help="Increase verbosity")
    parser.add_argument("--input", "-i", help="Input word")
    # TODO redefine limit, null, sep etc

    args = parser.parse_args(args or None)
    return args


if __name__ == "__main__":
    args = parseargs()
    prog = args.program.read()
    if args.program == sys.stdin:
        sys.stdin = open("/dev/tty", "r")
    word = args.input or input()
    main(prog, word, args.debug)
