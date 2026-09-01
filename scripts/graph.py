#!/usr/bin/env python3
"""Draw the kasten's link graph as an SVG.

Reads every note, follows the [[wikilinks]], lays the result out with a
force-directed simulation and writes docs/graph-light.svg and docs/graph-dark.svg
for the README. Standard library only, same as reset.py.

    python scripts/graph.py                   # regenerate both SVGs
    python scripts/graph.py --stats           # print counts and exit
    python scripts/graph.py --iterations 1500 # slower, tidier layout

The layout is seeded, so the same vault always produces the same picture.
"""
import argparse, math, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")
SKIP_DIRS = {".git", ".obsidian", ".trash", "_templates", "scripts", "docs"}
# Root navigation uses ordinary relative links, not wikilinks, so it has no edges.
SKIP_FILES = {"README.md", "CONTRIBUTING.md", "MOC.md"}

WIDTH, HEIGHT = 1200, 900
PAD = 40
LINK = re.compile(r"\[\[([^\]|#]+)")

# A node's colour is the ladder it belongs to; everything else is scaffolding.
LADDERS = (("01-systems", "systems"), ("02-ai", "ai"))

THEMES = {
    "light": dict(bg="#ffffff", edge="#1b1b1b", edge_op=0.26, halo="#ffffff",
                  systems="#5f7794", ai="#b3843f", other="#c2c2c2"),
    "dark":  dict(bg="#0d1117", edge="#c9d1d9", edge_op=0.22, halo="#0d1117",
                  systems="#7d9bc1", ai="#cfa367", other="#454c56"),
}


def collect():
    """Return (nodes, edges): note titles and the links between them."""
    titles, raw = {}, {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if not name.endswith(".md") or name in SKIP_FILES:
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            title = name[:-3]
            group = next((g for prefix, g in LADDERS if rel.startswith(prefix)), "other")
            titles[title] = group
            raw[title] = open(path, encoding="utf-8").read()

    edges = set()
    for title, text in raw.items():
        for target in LINK.findall(text):
            target = target.strip()
            if target in titles and target != title:
                edges.add(tuple(sorted((title, target))))
    return titles, sorted(edges)


def layout(nodes, edges, degree, iterations, seed=7):
    """Fruchterman-Reingold with a little gravity, so nothing drifts off-canvas."""
    rng = random.Random(seed)
    n = len(nodes)
    k = 1.05 * math.sqrt(WIDTH * HEIGHT / n)
    pos = {}
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / n
        r = rng.uniform(0.25, 1.0) * min(WIDTH, HEIGHT) / 2
        pos[node] = [WIDTH / 2 + r * math.cos(angle), HEIGHT / 2 + r * math.sin(angle)]

    temp = WIDTH / 8
    cool = temp / (iterations + 1)
    order = list(nodes)
    for step in range(iterations):
        disp = {node: [0.0, 0.0] for node in order}
        for i, a in enumerate(order):
            ax, ay = pos[a]
            for b in order[i + 1:]:
                dx, dy = ax - pos[b][0], ay - pos[b][1]
                d2 = dx * dx + dy * dy
                if d2 < 0.01:
                    dx, dy, d2 = rng.uniform(-1, 1), rng.uniform(-1, 1), 1.0
                force = k * k / d2
                disp[a][0] += dx * force
                disp[a][1] += dy * force
                disp[b][0] -= dx * force
                disp[b][1] -= dy * force
        for a, b in edges:
            dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
            d = math.hypot(dx, dy) or 0.01
            force = d / k
            disp[a][0] -= dx * force
            disp[a][1] -= dy * force
            disp[b][0] += dx * force
            disp[b][1] += dy * force
        for node in order:
            dx, dy = disp[node]
            # gravity: the fewer links a note has, the harder it is pulled in,
            # so a lone note sits at the edge of the mass instead of the canvas
            g = 0.02 + 0.25 / (1 + degree[node])
            dx += (WIDTH / 2 - pos[node][0]) * g
            dy += (HEIGHT / 2 - pos[node][1]) * g
            d = math.hypot(dx, dy) or 1.0
            scale = min(d, temp) / d
            pos[node][0] = min(max(pos[node][0] + dx * scale, 0.0), WIDTH)
            pos[node][1] = min(max(pos[node][1] + dy * scale, 0.0), HEIGHT)
        temp -= cool
    return pos


def orient(pos):
    """Rotate the layout so its long axis runs horizontally.

    Force-directed output lands at an arbitrary angle; without this the graph
    sits diagonally and wastes two corners of the canvas.
    """
    n = len(pos)
    cx = sum(p[0] for p in pos.values()) / n
    cy = sum(p[1] for p in pos.values()) / n
    sxx = sum((p[0] - cx) ** 2 for p in pos.values())
    syy = sum((p[1] - cy) ** 2 for p in pos.values())
    sxy = sum((p[0] - cx) * (p[1] - cy) for p in pos.values())
    theta = 0.5 * math.atan2(2 * sxy, sxx - syy)
    cos, sin = math.cos(-theta), math.sin(-theta)
    return {node: [(p[0] - cx) * cos - (p[1] - cy) * sin,
                   (p[0] - cx) * sin + (p[1] - cy) * cos]
            for node, p in pos.items()}


def fit(pos):
    """Scale the finished layout into the canvas with an even margin."""
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    spanx, spany = max(xs) - min(xs) or 1, max(ys) - min(ys) or 1
    scale = min((WIDTH - 2 * PAD) / spanx, (HEIGHT - 2 * PAD) / spany)
    offx = (WIDTH - spanx * scale) / 2 - min(xs) * scale
    offy = (HEIGHT - spany * scale) / 2 - min(ys) * scale
    return {n: (p[0] * scale + offx, p[1] * scale + offy) for n, p in pos.items()}


def radius(degree):
    return round(2.4 + 1.55 * math.sqrt(degree), 2)


def render(pos, edges, groups, degree, theme):
    t = THEMES[theme]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}" role="img" '
        f'aria-label="Link graph of the Fundamentals Kasten">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{t["bg"]}"/>',
        f'<g stroke="{t["edge"]}" stroke-opacity="{t["edge_op"]}" stroke-width="0.9">',
    ]
    for a, b in edges:
        ax, ay = pos[a]
        bx, by = pos[b]
        out.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}"/>')
    out.append("</g>")
    out.append(f'<g stroke="{t["halo"]}" stroke-width="1.2">')
    # biggest last, so hubs sit on top of the notes they connect
    for node in sorted(pos, key=lambda n: degree[n]):
        x, y = pos[node]
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius(degree[node])}" '
                   f'fill="{t[groups[node]]}"><title>{esc(node)}</title></circle>')
    out.append("</g></svg>")
    return "\n".join(out)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=900)
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()

    groups, edges = collect()
    degree = {n: 0 for n in groups}
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1

    if args.stats:
        counts = {g: sum(1 for v in groups.values() if v == g) for g in ("systems", "ai", "other")}
        top = sorted(degree.items(), key=lambda kv: -kv[1])[:10]
        print(f"{len(groups)} notes, {len(edges)} links  {counts}")
        print(f"orphans: {sum(1 for d in degree.values() if d == 0)}")
        print("most linked:")
        for name, d in top:
            print(f"  {d:4}  {name}")
        sys.exit()

    print(f"laying out {len(groups)} notes and {len(edges)} links...", file=sys.stderr)
    pos = fit(orient(layout(sorted(groups), edges, degree, args.iterations)))
    os.makedirs(OUT, exist_ok=True)
    for theme in THEMES:
        path = os.path.join(OUT, f"graph-{theme}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(render(pos, edges, groups, degree, theme))
        print(os.path.relpath(path, ROOT))
