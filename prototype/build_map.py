#!/usr/bin/env python3
"""Bake blueprint_walls.txt -> map2d.js (interior flood-filled) and validate the
patient-journey anchors are reachable through the blueprint's door gaps."""
import json, pathlib, collections

ROOT = pathlib.Path(__file__).parent
raw = (ROOT / "blueprint_walls.txt").read_text().strip().splitlines()
grid = [[int(v) for v in line.split()] for line in raw if line.strip()]
H = len(grid)
W = max(len(r) for r in grid)
for r in grid:                      # pad short rows with wall
    r += [1] * (W - len(r))
print(f"grid {W} x {H}")

WALL = lambda x, y: grid[y][x] == 1
OPEN = lambda x, y: 0 <= x < W and 0 <= y < H and grid[y][x] == 0

# ---- exterior void: the black bottom-left region in the blueprint.
# walls.txt leaves it un-walled, so it must be masked out or the flood leaks in.
def is_void(x, y):
    return y >= 39 and x <= 47

# ---- flood-fill the interior from the reception desk (one true seed) ----
SEED = (56, 58)
interior = set()
def flood(sx, sy):
    if not OPEN(sx, sy) or is_void(sx, sy): return
    q = collections.deque([(sx,sy)]); interior.add((sx,sy))
    while q:
        x,y = q.popleft()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny = x+dx,y+dy
            if OPEN(nx,ny) and not is_void(nx,ny) and (nx,ny) not in interior:
                interior.add((nx,ny)); q.append((nx,ny))
flood(*SEED)
print(f"interior cells: {len(interior)}")

# ---- snap an anchor to the nearest reachable interior cell ----
def snap(x, y):
    best=None; bd=1e9
    for (ix,iy) in interior:
        d=(ix-x)**2+(iy-y)**2
        if d<bd: bd=d; best=(ix,iy)
    return best

ANCHORS = [
    ("here",   "front desk — checked in",          (56,58)),
    ("vision", "Vision check room",                (83,46)),
    ("hvf",    "HVF visual-field test",            (58,46)),
    ("octwait","tertiary waiting — waiting for OCT",(63,9)),
    ("oct",    "OCT scan room",                    (84,8)),
    ("drwait", "quaternary waiting — waiting for Dr",(26,22)),
    ("doctor", "with the doctor — exam room",      (12,30)),
    ("billed", "back at the desk — billed",        (56,58)),
]
snapped = [(s, w, snap(*t)) for s,w,t in ANCHORS]
for (s,w,t),(s2,w2,sn) in zip(ANCHORS, snapped):
    print(f"  {s:8} req{t} -> snap{sn}")

# ---- BFS path length between consecutive anchors (validation) ----
def bfs(a, b):
    q=collections.deque([a]); prev={a:None}
    while q:
        x,y=q.popleft()
        if (x,y)==b:
            n=0; c=b
            while c: n+=1; c=prev[c]
            return n
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if OPEN(nx,ny) and (nx,ny) not in prev:
                prev[(nx,ny)]=(x,y); q.append((nx,ny))
    return None
print("leg reachability:")
ok=True
for i in range(len(snapped)-1):
    a=snapped[i][2]; b=snapped[i+1][2]
    L=bfs(a,b)
    print(f"  {snapped[i][0]:8} -> {snapped[i+1][0]:8}  len={L}")
    if L is None: ok=False
print("ALL LEGS REACHABLE" if ok else "!!! SOME LEG UNREACHABLE")

# ---- emit map2d.js : '#'=wall '.'=interior-floor ' '=void ----
rows=[]
for y in range(H):
    line=[]
    for x in range(W):
        if grid[y][x]==1: line.append('#')
        elif (x,y) in interior: line.append('.')
        else: line.append(' ')
    rows.append(''.join(line))
js = "window.CLINIC_MAP=" + json.dumps({"w":W,"h":H,"rows":rows}) + ";\n"
(ROOT/"map2d.js").write_text(js)
print("wrote map2d.js")
