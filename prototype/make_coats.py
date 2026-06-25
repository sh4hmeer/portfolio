# Build white-coat (doctor) variants of the LimeZu walk sheets by recolouring the
# shirt band to white. Output: assets/limezu/<Name>_coat.png, loaded by clinic2d.html.
# Re-run after changing the base character art.  Usage: python make_coats.py
from PIL import Image

NAMES = ['Adam', 'Amelia', 'Bob', 'Alex']
SRC = 'assets/limezu/%s_16x16.png'
OUT = 'assets/limezu/%s_coat.png'

def is_skin(r, g, b):
    return r > 150 and 90 < g < 205 and b < 175 and r > g >= b - 12

def whiten(r, g, b):
    L = 0.3*r + 0.59*g + 0.11*b
    if L < 80:                       # outline / deep fold -> keep a cool grey
        return (80, 86, 99, 255)
    t = max(0.0, min(1.0, (L - 80) / (150 - 80)))
    base = int(205 + t * 50)         # 205..255, shading preserved
    return (max(0, base - 5), max(0, base - 2), min(255, base + 4), 255)

def make(name):
    im = Image.open(SRC % name).convert('RGBA')
    px = im.load(); W, H = im.size
    out = im.copy(); o = out.load()
    for Y in range(H):
        if not (22 <= Y % 32 <= 28):  # shirt band within each 32px frame
            continue
        for X in range(W):
            r, g, b, a = px[X, Y]
            if a < 200 or is_skin(r, g, b):
                continue
            o[X, Y] = whiten(r, g, b)
    out.save(OUT % name)
    print('wrote', OUT % name)

if __name__ == '__main__':
    for n in NAMES:
        make(n)
