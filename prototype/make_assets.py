"""
Generates original (CC0) pixel-art assets for the walkable clinic:
  assets/tiles.png  - 16x16 tile atlas (8 cols)
  assets/char.png   - 16x24 character sheet, rows = down/up/left/right, 3 frames each
                      shirt drawn in magenta key (#ff00ff / #b400b4) for JS recolour.
Run:  python make_assets.py
"""
from PIL import Image
import os

S = 16
ATLAS_COLS = 8
os.makedirs("assets", exist_ok=True)

# ---------- palette ----------
P = {
  'void':(0,0,0,0),
  'hall':(196,205,214,255),'hall_l':(208,216,224,255),'hall_d':(176,186,197,255),
  'room':(226,217,196,255),'room_l':(236,228,209,255),'room_d':(206,196,172,255),
  'roomb':(200,214,224,255),'roomb_d':(178,196,210,255),
  'check_a':(228,232,238,255),'check_b':(150,164,182,255),
  'wall':(150,165,184,255),'wall_hi':(176,190,206,255),'wall_lo':(96,110,132,255),'wall_cap':(112,126,148,255),
  'base':(70,82,102,255),
  'wood':(178,140,92,255),'wood_d':(150,116,74,255),'wood_l':(200,166,118,255),
  'chair':(74,118,170,255),'chair_d':(56,94,140,255),'chair_l':(104,148,196,255),
  'plantpot':(150,96,64,255),'plantpot_d':(126,78,52,255),
  'leaf':(74,162,98,255),'leaf_d':(54,134,78,255),'leaf_l':(110,190,128,255),
  'mach':(234,240,246,255),'mach_d':(198,208,220,255),'mach_head':(74,84,104,255),'screen':(58,150,206,255),'screen_d':(40,110,160,255),
  'stool':(96,104,120,255),'stool_d':(74,82,98,255),
  'rug':(196,86,80,255),'rug_d':(168,66,62,255),
  'glass':(120,180,210,255),'glass_d':(92,150,182,255),
  'metal':(120,130,148,255),
  'dark':(34,40,50,255),
}

def newt():
    return Image.new("RGBA",(S,S),P['void'])

def fill(img,c):
    for y in range(S):
        for x in range(S):
            img.putpixel((x,y),c)

def rect(img,x0,y0,x1,y1,c):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if 0<=x<S and 0<=y<S: img.putpixel((x,y),c)

def px(img,x,y,c):
    if 0<=x<S and 0<=y<S: img.putpixel((x,y),c)

# ---------- floor tiles ----------
def t_hall():
    t=newt(); fill(t,P['hall'])
    for x in range(S): px(t,x,0,P['hall_d']);
    for y in range(S): px(t,0,y,P['hall_d'])
    # subtle lino speckle / seam
    for (x,y) in [(4,5),(11,9),(7,12),(13,3)]: px(t,x,y,P['hall_l'])
    return t
def t_room():
    t=newt(); fill(t,P['room'])
    for x in range(S): px(t,x,0,P['room_d'])
    for y in range(S): px(t,0,y,P['room_d'])
    for (x,y) in [(5,6),(10,11),(12,4)]: px(t,x,y,P['room_l'])
    return t
def t_roomb():
    t=newt(); fill(t,P['roomb'])
    for x in range(S): px(t,x,0,P['roomb_d'])
    for y in range(S): px(t,0,y,P['roomb_d'])
    return t
def t_check():
    t=newt()
    for y in range(S):
        for x in range(S):
            c=P['check_a'] if ((x//4)+(y//4))%2==0 else P['check_b']
            t.putpixel((x,y),c)
    return t

# ---------- wall ----------
def t_wall():
    t=newt(); fill(t,P['wall'])
    rect(t,0,0,S-1,2,P['wall_cap'])      # top cap
    rect(t,0,0,S-1,0,P['wall_hi'])       # hilite
    rect(t,0,S-2,S-1,S-1,P['wall_lo'])   # bottom shade
    # faint panel seam
    for y in range(3,S-2): px(t,8,y,P['wall_lo'])
    return t
def t_wall_win():
    t=t_wall()
    rect(t,3,5,12,11,P['glass']); rect(t,3,5,12,5,P['glass_d']); rect(t,3,8,12,8,P['glass_d'])
    px(t,7,8,P['glass_d']); rect(t,3,5,3,11,P['metal']); rect(t,12,5,12,11,P['metal'])
    return t

# ---------- furniture ----------
def t_deskH():   # horizontal counter/desk segment
    t=newt(); rect(t,0,4,S-1,S-1,P['wood'])
    rect(t,0,4,S-1,5,P['wood_l']); rect(t,0,S-1,S-1,S-1,P['wood_d'])
    for x in range(0,S,5): rect(t,x,7,x,S-2,P['wood_d'])
    return t
def t_chair():   # waiting chair, faces down (toward viewer)
    t=newt()
    rect(t,3,3,12,6,P['chair_d'])        # backrest
    rect(t,3,7,12,12,P['chair'])         # seat
    rect(t,3,7,12,7,P['chair_l'])
    rect(t,4,13,5,15,P['dark']); rect(t,10,13,11,15,P['dark'])  # legs
    return t
def t_stool():
    t=newt(); rect(t,5,6,10,10,P['stool']); rect(t,5,6,10,6,P['stool']);
    rect(t,6,11,6,14,P['stool_d']); rect(t,9,11,9,14,P['stool_d'])
    return t
def t_plant():
    t=newt()
    rect(t,5,11,10,14,P['plantpot']); rect(t,5,14,10,14,P['plantpot_d'])
    rect(t,4,4,11,10,P['leaf']); rect(t,4,4,11,5,P['leaf_l'])
    for (x,y) in [(6,6),(9,7),(7,9),(5,8),(10,9)]: px(t,x,y,P['leaf_d'])
    px(t,7,2,P['leaf']); px(t,8,3,P['leaf'])
    return t
def t_exam_top():  # recliner upper (headrest)
    t=newt(); rect(t,3,6,12,15,P['chair']); rect(t,3,6,12,7,P['chair_l'])
    rect(t,5,8,10,11,P['chair_l'])   # pillow
    rect(t,3,6,3,15,P['chair_d']); rect(t,12,6,12,15,P['chair_d'])
    return t
def t_exam_bot():  # recliner lower (seat/legrest) + base
    t=newt(); rect(t,3,0,12,7,P['chair']); rect(t,3,7,12,9,P['chair_d'])
    rect(t,6,9,9,14,P['metal'])      # pedestal
    rect(t,4,14,11,15,P['stool_d'])  # base
    return t
def t_machine_top():  # eye machine head
    t=newt(); rect(t,2,5,13,15,P['mach']); rect(t,2,5,13,6,P['mach'])
    rect(t,4,2,11,7,P['mach_head'])  # head unit
    rect(t,6,7,9,11,P['mach_head'])  # chin column
    rect(t,2,5,2,15,P['mach_d']); rect(t,13,5,13,15,P['mach_d'])
    return t
def t_machine_bot():  # machine table/base
    t=newt(); rect(t,2,0,13,6,P['mach']); rect(t,2,6,13,8,P['mach_d'])
    rect(t,4,8,5,15,P['mach_d']); rect(t,10,8,11,15,P['mach_d'])
    return t
def t_monitor():
    t=newt(); rect(t,3,3,12,10,P['mach_head']); rect(t,4,4,11,9,P['screen'])
    rect(t,4,4,11,4,P['screen_d']); rect(t,7,11,8,12,P['mach_head']); rect(t,5,13,10,14,P['mach_d'])
    return t
def t_rug():
    t=newt(); fill(t,P['rug']); rect(t,0,0,S-1,0,P['rug_d']); rect(t,0,0,0,S-1,P['rug_d'])
    rect(t,2,2,S-3,S-3,P['rug']);
    for x in range(2,S-2,3): px(t,x,2,P['rug_d']); px(t,x,S-3,P['rug_d'])
    return t

TILES = [
  ('void', newt),('hall',t_hall),('room',t_room),('roomb',t_roomb),('check',t_check),
  ('wall',t_wall),('wall_win',t_wall_win),('door',t_hall),
  ('deskH',t_deskH),('chair',t_chair),('stool',t_stool),('plant',t_plant),
  ('exam_top',t_exam_top),('exam_bot',t_exam_bot),('mach_top',t_machine_top),('mach_bot',t_machine_bot),
  ('monitor',t_monitor),('rug',t_rug),
]

def build_atlas():
    cols=ATLAS_COLS; rows=(len(TILES)+cols-1)//cols
    atlas=Image.new("RGBA",(cols*S,rows*S),(0,0,0,0))
    index={}
    for i,(name,fn) in enumerate(TILES):
        cx=(i%cols)*S; cy=(i//cols)*S
        atlas.paste(fn(),(cx,cy)); index[name]=i
    atlas.save("assets/tiles.png")
    return index

# ---------- character 16x24 ----------
CW,CH=16,24
SK=(236,196,156,255); SKd=(206,164,124,255)
HR=(74,52,40,255); HRl=(96,70,52,255)
SH=(255,0,255,255); SHd=(180,0,180,255)      # shirt key colours
PA=(64,74,96,255); PAd=(48,56,74,255)
SHO=(32,36,46,255)
OUT=(28,30,38,255)

def cnew(): return Image.new("RGBA",(CW,CH),(0,0,0,0))
def cpx(img,x,y,c):
    if 0<=x<CW and 0<=y<CH: img.putpixel((x,y),c)
def crect(img,x0,y0,x1,y1,c):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1): cpx(img,x,y,c)

def shadow(img):
    for x in range(5,11): cpx(img,x,23,(0,0,0,70))
    for x in range(6,10): cpx(img,x,22,(0,0,0,50))

def legs(img,phase):
    # phase: 0 stand, 1 left fwd, 2 right fwd
    ly=18
    lx,rx = 6,9
    if phase==1: crect(img,lx,ly,lx+1,21,PA); crect(img,rx,ly,rx+1,20,PAd)
    elif phase==2: crect(img,lx,ly,lx+1,20,PAd); crect(img,rx,ly,rx+1,21,PA)
    else: crect(img,lx,ly,lx+1,21,PA); crect(img,rx,ly,rx+1,21,PA)
    crect(img,lx,22,lx+1,22,SHO); crect(img,rx,22,rx+1,22,SHO)

def body_front(img):
    crect(img,5,11,10,18,SH); crect(img,5,11,10,11,SHd)   # shirt
    crect(img,4,12,4,16,SK); crect(img,11,12,11,16,SK)    # arms
    crect(img,4,16,4,16,SKd); crect(img,11,16,11,16,SKd)

def head_front(img):
    crect(img,5,3,10,9,SK); crect(img,5,9,10,9,SKd)
    crect(img,5,2,10,4,HR); crect(img,4,3,4,5,HR); crect(img,11,3,11,5,HR); crect(img,5,2,10,2,HRl)
    cpx(img,6,6,OUT); cpx(img,9,6,OUT)                    # eyes
    cpx(img,7,8,SKd)

def head_back(img):
    crect(img,5,3,10,9,HR); crect(img,5,2,10,2,HRl); crect(img,4,3,4,6,HR); crect(img,11,3,11,6,HR)
    crect(img,7,8,8,9,SKd)  # neck hint

def body_back(img):
    crect(img,5,11,10,18,SHd);
    crect(img,4,12,4,16,SK); crect(img,11,12,11,16,SK)

def head_side(img,face_left):
    crect(img,5,3,10,9,SK); crect(img,5,9,10,9,SKd)
    crect(img,5,2,10,3,HR); crect(img,5,2,10,2,HRl)
    if face_left:
        crect(img,4,3,4,7,HR); cpx(img,6,6,OUT)
    else:
        crect(img,11,3,11,7,HR); cpx(img,9,6,OUT)

def body_side(img,face_left):
    crect(img,5,11,10,18,SH); crect(img,5,11,10,11,SHd)
    if face_left: crect(img,5,12,5,16,SK)
    else: crect(img,10,12,10,16,SK)

def make_char():
    sheet=Image.new("RGBA",(CW*3,CH*4),(0,0,0,0))
    dirs=['down','up','left','right']
    for r,d in enumerate(dirs):
        for f in range(3):
            img=cnew(); shadow(img); legs(img,f)
            if d=='down': body_front(img); head_front(img)
            elif d=='up': body_back(img); head_back(img)
            elif d=='left': body_side(img,True); head_side(img,True)
            else: body_side(img,False); head_side(img,False)
            sheet.paste(img,(f*CW,r*CH))
    sheet.save("assets/char.png")

def emit_data_js(idx):
    # base64-inline the PNGs so the engine can getImageData (recolor) under file:// without taint
    import base64, json
    def b64(path):
        return base64.b64encode(open(path,"rb").read()).decode()
    js = ("window.CLINIC_ASSETS={\n"
          f"  tiles:'data:image/png;base64,{b64('assets/tiles.png')}',\n"
          f"  char:'data:image/png;base64,{b64('assets/char.png')}',\n"
          f"  index:{json.dumps(idx)}\n"
          "};\n")
    open("assets_data.js","w").write(js)

if __name__=="__main__":
    idx=build_atlas()
    make_char()
    import json
    json.dump(idx,open("assets/tiles_index.json","w"),indent=0)
    emit_data_js(idx)
    print("tiles:",len(TILES),"->",idx)
    print("char sheet: assets/char.png (3 frames x 4 dirs)")
    print("wrote assets_data.js (inlined base64)")
