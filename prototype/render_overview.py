#!/usr/bin/env python3
"""Full-map overview of the baked clinic: void=black, wall=pink, floor=cream,
plus room labels, journey anchors and the BFS flow path — to compare vs blueprint."""
import json, collections
from PIL import Image, ImageDraw, ImageFont

s=open('map2d.js').read(); d=json.loads(s[s.index('{'):s.rindex('}')+1])
W,H,rows=d['w'],d['h'],d['rows']
T=14
img=Image.new('RGB',(W*T,H*T),(8,11,17))
dr=ImageDraw.Draw(img)
grid=[[0]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        ch=rows[y][x]
        if ch=='#':
            dr.rectangle([x*T,y*T,x*T+T-1,y*T+T-1],fill=(244,140,170)); grid[y][x]=1
        elif ch=='.':
            dr.rectangle([x*T,y*T,x*T+T-1,y*T+T-1],fill=(235,228,205))

# BFS over walkable (walls block) to trace the journey
def walk(x,y): return 0<=x<W and 0<=y<H and rows[y][x]=='.'
def snap(x,y):
    if walk(x,y): return (x,y)
    for r in range(1,12):
        for dy in range(-r,r+1):
            for dx in range(-r,r+1):
                if walk(x+dx,y+dy): return (x+dx,y+dy)
    return (x,y)
def bfs(a,b):
    q=collections.deque([a]); prev={a:None}
    while q:
        c=q.popleft()
        if c==b:
            out=[];k=c
            while k:out.append(k);k=prev[k]
            return out[::-1]
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            n=(c[0]+dx,c[1]+dy)
            if walk(*n) and n not in prev: prev[n]=c;q.append(n)
    return []

ANCH=[('here',(56,58)),('vision',(83,46)),('hvf',(58,46)),('octwait',(63,9)),
      ('oct',(84,8)),('drwait',(26,22)),('doctor',(12,30)),('billed',(56,58))]
cur=snap(72,64)
for name,t in ANCH:
    dst=snap(*t); p=bfs(cur,dst)
    for (x,y) in p:
        dr.ellipse([x*T+5,y*T+5,x*T+9,y*T+9],fill=(80,200,255))
    cur=dst
for name,t in ANCH:
    x,y=snap(*t)
    dr.ellipse([x*T+2,y*T+2,x*T+T-2,y*T+T-2],outline=(255,80,80),width=2)

LABELS=[('EXAM',9,4),('EXAM',24,4),('EXAM',33,4),('SCAN',42,4),('TERTIARY WAIT',62,5),
 ('oct1',82,4),('oct3',82,14),('vis4',82,20),('EXAM',58,18),('oct2',67,19),
 ('vis3',67,31),('SECONDARY',80,29),('SURGICAL',58,31),('hvf',55,44),('vis2',67,44),
 ('vis1',81,44),('RECEPTION',70,52),('QUATERNARY',24,20),
 ('EXAM',11,30),('EXAM',22,30),('EXAM',31,30),('EXAM',42,30)]
try: f=ImageFont.truetype('arial.ttf',11)
except: f=ImageFont.load_default()
for txt,x,y in LABELS:
    dr.text((x*T-len(txt)*3,y*T),txt,fill=(20,20,30),font=f)
img.save('_overview.png'); print('wrote _overview.png',img.size)
