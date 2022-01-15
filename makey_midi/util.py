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

if __name__ == '__main__':
    pass

