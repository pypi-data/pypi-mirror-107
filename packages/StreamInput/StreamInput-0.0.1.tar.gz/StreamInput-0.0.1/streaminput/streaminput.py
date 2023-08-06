#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import selectors


def _echo(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()

def streaminput(prompt=None, timeout=None):
    if prompt is not None:
        _echo(prompt)
    selector = selectors.DefaultSelector()
    selector.register(sys.stdin, selectors.EVENT_READ)
    events = selector.select(timeout=timeout)
    if events:
        key, _ = events[0]
        data = key.fileobj.readline().strip()
    else:
        _echo('\n')
        data = None
    selector.close()
    return data
