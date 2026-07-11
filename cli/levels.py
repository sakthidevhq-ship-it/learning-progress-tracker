"""Assign learning-depth levels to resources.

A resource's level is its intrinsic difficulty floor (complexity +
prerequisite-concept load + size nudge), deepened by prerequisite
chains. "No incoming edge" does NOT mean foundational — an advanced
paper whose prerequisites aren't in the collection still floors at
its intrinsic level. Cycles (resources mutually teaching/requiring
each other's concepts) are condensed via Tarjan SCC so constraint
propagation always terminates.
"""

from collections import deque

COMPLEXITY_BASE = {"beginner": 0.0, "intermediate": 1.0, "advanced": 2.0}
SIZE_NUDGE = {"quick-read": 0.0, "medium": 0.15, "deep-dive": 0.3}
PUSH_CAP = 2.0  # max rise above a node's own intrinsic floor via edges


def intrinsic_floor(complexity, prereq_concept_count, size):
    base = COMPLEXITY_BASE.get(complexity, 1.0)
    load = min(2.0, prereq_concept_count / 3.0)
    return base + load + SIZE_NUDGE.get(size, 0.0)


def tarjan_scc(n, adj):
    """Iterative Tarjan. Returns (comp id per node, component count)."""
    UNVISITED = -1
    index = [UNVISITED] * n
    low = [0] * n
    on = [False] * n
    comp = [UNVISITED] * n
    stack = []
    counter = 0
    cid = 0
    for root in range(n):
        if index[root] != UNVISITED:
            continue
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on[root] = True
        work = [(root, iter(adj[root]))]
        while work:
            v, it = work[-1]
            advanced = False
            for w in it:
                if index[w] == UNVISITED:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on[w] = True
                    work.append((w, iter(adj[w])))
                    advanced = True
                    break
                elif on[w]:
                    low[v] = min(low[v], index[w])
            if advanced:
                continue
            work.pop()
            if low[v] == index[v]:
                while True:
                    w = stack.pop()
                    on[w] = False
                    comp[w] = cid
                    if w == v:
                        break
                cid += 1
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
    return comp, cid


def assign_levels(nodes, edges):
    """nodes: list of {complexity, prereq_count, size}.
    edges: list of (teacher_idx, dependent_idx).
    Returns float level per node."""
    n = len(nodes)
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)

    comp, ncomp = tarjan_scc(n, adj)
    members = [[] for _ in range(ncomp)]
    for v, c in enumerate(comp):
        members[c].append(v)

    floors = [
        intrinsic_floor(nd.get("complexity"), nd.get("prereq_count", 0), nd.get("size"))
        for nd in nodes
    ]
    # A cycle inherits the depth of its hardest member
    cfloor = [max(floors[v] for v in mem) for mem in members]

    # Condensation DAG
    cadj = [set() for _ in range(ncomp)]
    cindeg = [0] * ncomp
    for u, v in edges:
        cu, cv = comp[u], comp[v]
        if cu != cv and cv not in cadj[cu]:
            cadj[cu].add(cv)
            cindeg[cv] += 1

    # Kahn topo order with soft capped push: an edge places the child
    # above its predecessor, but never more than PUSH_CAP above the
    # child's own floor (one bad edge can't rocket a beginner item deep)
    clevel = list(cfloor)
    q = deque(c for c in range(ncomp) if cindeg[c] == 0)
    while q:
        c = q.popleft()
        for d in cadj[c]:
            proposed = min(clevel[c] + 1.0, cfloor[d] + PUSH_CAP)
            if proposed > clevel[d]:
                clevel[d] = proposed
            cindeg[d] -= 1
            if cindeg[d] == 0:
                q.append(d)

    # Fan cycle members across a 0.25 band by intrinsic difficulty
    levels = [0.0] * n
    for c, mem in enumerate(members):
        base = clevel[c]
        order = sorted(mem, key=lambda v: floors[v])
        m = len(order)
        for i, v in enumerate(order):
            levels[v] = base + (0.0 if m == 1 else 0.25 * i / (m - 1))
    return levels
