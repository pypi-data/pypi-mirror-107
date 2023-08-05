# SPDX-License-Identifier: GPL-3.0-or-later

# Copyright (C) 2020 Michał Góral.

from i3ipc.aio import Connection
from i3ipc import Event

import asyncio
import collections
import argparse

FLOATING_MODES = ('auto_on', 'user_on')
STACKMARK = '"__i3a_stack"'
args = None

def prepare_args():
    parser = argparse.ArgumentParser(
        description='i3a - i3 automation'
    )

    parser.add_argument('--stack', choices=('dwm', 'i3'), default='i3',
                        help='choose visual type of stacking')
    parser.add_argument('--stack-size', type=int, default=50,
                        help='percentage size of stack area')

    return parser.parse_args()

# Depth-first traversal of leaf nodes. It is more useful for determining which
# node on the stack is the last one (if user decided to e.g. split some middle
# stack windows, breadth-first, implemented by i3ipc-python, would yield
# incorrect results and new windows would be created in that split)
def leaves_dfs(root):
    stack = collections.deque([root])
    while len(stack) > 0:
        n = stack.pop()
        if not n.nodes and n.type == "con" and n.parent.type != "dockarea":
            yield n
        stack.extend(reversed(n.nodes))


def get_workspaces(tree):
    workspaces = {}
    for window in leaves_dfs(tree):
        w = window.workspace()
        if w is None:
            continue
        workspaces.setdefault(w.name, []).append(window)
    return workspaces


def tiled_nodes(tree, wsname):
    workspaces = get_workspaces(tree)
    ws = workspaces.get(wsname, [])
    return [l for l in ws if l.floating not in FLOATING_MODES]


async def make_stack(i3, node):
    # this works only when there are exactly 2 nodes, which is a caller
    # responsibility to check
    await i3.command('[con_id="{}"] split vertical'.format(node.id))

    if args.stack == 'i3':
        await i3.command('[con_id="{}"] layout stacking'.format(node.id))


def master_stack(tree, node):
    cont = tree.find_by_id(node.id)
    if cont is None:
        return None, None

    if cont.floating in FLOATING_MODES:
        return None, None

    wsname = cont.workspace().name
    tiled = tiled_nodes(tree, wsname)

    if not tiled:
        return None, None

    master = tiled[0]
    stack = tiled[1:]
    return master, stack


async def win_close(i3, e):
    tree = await i3.get_tree()
    master, stack = master_stack(tree, tree.find_focused())

    if not master:
        return

    if master and not stack:
        await i3.command('[con_id="{}"] split horizontal'.format(master.id))
        return

    await i3.command('[con_id="{}"] move left'.format(master.id))
    await i3.command('[con_id="{}"] resize set {} ppt 0 ppt'.format(stack[-1].id, args.stack_size))


async def win_stack(i3, e):
    tree = await i3.get_tree()
    master, stack = master_stack(tree, e.container)

    if not master or not stack:
        return

    curr = tree.find_by_id(e.container.id)

    if len(stack) == 0:
        await i3.command('[con_id="{}"] split horizontal'.format(master.id))
    elif len(stack) == 1:
        await make_stack(i3, stack[-1])
        await i3.command('[con_id="{}"] resize set {} ppt 0 ppt'.format(stack[-1].id, args.stack_size))
    elif len(stack) > 1:
        await i3.command('[con_id="{}"] mark --add {}'.format(stack[-1].id, STACKMARK))
        await i3.command('[con_id="{}"] move window to mark {}'.format(curr.id, STACKMARK))
        await i3.command('[con_id="{}"] focus'.format(curr.id))  # moving to mark doesn't move focus


async def win_move(i3, e):
    tree = await i3.get_tree()

    curr = tree.find_by_id(e.container.id)
    foc = tree.find_focused()

    if foc.workspace() == curr.workspace():
        return

    master, stack = master_stack(tree, e.container)

    if not master or not stack:
        return

    if len(stack) == 0:
        await i3.command('[con_id="{}"] split horizontal'.format(master.id))
    elif len(stack) == 1:
        await make_stack(i3, stack[-1])
        await i3.command('[con_id="{}"] resize set {} ppt 0 ppt'.format(stack[-1].id, args.stack_size))
    elif len(stack) > 1:
        await i3.command('[con_id="{}"] mark --add {}'.format(stack[-1].id, STACKMARK))
        await i3.command('[con_id="{}"] move window to mark {}'.format(curr.id, STACKMARK))


async def amain():
    i3 = await Connection(auto_reconnect=True).connect()
    i3.on(Event.WINDOW_CLOSE, win_close)
    i3.on(Event.WINDOW_NEW, win_stack)
    i3.on(Event.WINDOW_MOVE, win_move)
    await i3.main()


def main():
    global args
    args = prepare_args()
    asyncio.get_event_loop().run_until_complete(amain())
    return 0
