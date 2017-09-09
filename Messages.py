#!/usr/bin/env python3

from sys import stderr

def __info(*args, **kargs):
    print("[INFO]", *args, **kargs, file=stderr)

def __error(*args, **kargs):
    print("[ERROR]", *args, **kargs, file=stderr)
    exit(-1)

def __result(*args, **kargs):
    print(args, *args, **kargs, file=stderr)

def __warning(*args, **kargs):
    print("[WARN]", *args, **kargs, file=stderr)


INFO     = __info
ERROR    = __error
RESULT   = __result
WARNING  = __warning
