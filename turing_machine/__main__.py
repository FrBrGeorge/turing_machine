#!/usr/bin/env python3
import argparse
import sys
from . import Machine

HELPURL = "https://cmcmsu.info/1course/alg.schema.mt.htm"
RUNLIMIT = 32768

def run(mt, limit=RUNLIMIT):
    sw = max(len(str(s)) for s in mt.prog.states)
    trace = []
    for state, symbol in mt:
        info = f"{state:>{sw}}:{symbol}"
        if run.args.verbose > 1:
            print(f"{' ' * len(info)} {mt.tape}", file=sys.stderr)
            print(f"{info} {mt.tape.mark}", file=sys.stderr)
        elif run.args.verbose > 0 or run.args.debug:
            print(mt.tape, file=sys.stderr)
            print(mt.tape.mark, file=sys.stderr)
        if run.args.debug:
            match input(f"{info} -> {mt.prog.get((state, symbol), "UNKNOWN")}> "):
                case "p":
                    print(mt.prog)
                case "q":
                    return str(mt.tape)
                case "b" if len(trace) > 1:
                    trace.pop()
                    mt.state, mt.tape.content, mt.tape.current = trace[-1]
                    continue
        trace.append((state, mt.tape.content, mt.tape.current))
        if len(trace) >= limit:
            raise RuntimeError(f"Limit of {limit} steps is reached, still running")
    return str(mt.tape)

def execute(prog, word, debug):
    try:
        print(run(Machine(prog, word)))
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


def main():
    run.args = parseargs()
    prog = run.args.program.read()
    if run.args.program == sys.stdin:
        sys.stdin = open("/dev/tty", "r")
    word = run.args.input or input()
    execute(prog, word, run.args.debug)


if __name__ == "__main__":
    main()
