#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# Utility functions.
#

import os

def resolve_path(parent_dir, p):
    if not os.path.isabs(p):
        p = os.path.join(parent_dir, p)
    return p

def json_get(data, key, required = True, def_val = None, context = None):
    r = def_val
    if key in data:
        r = data[key]
    elif def_val == None and required:
        if context == None:
            context = ''
        raise ValueError('required value {} {} not specified'.format(context, key))
    return r

def json_gets(data, valmap, required = False, context = None):
    r = {k:json_get(data, k, required = required, def_val = valmap[k], context = context) for k in valmap}
    return r

if __name__ == '__main__':
    pass

