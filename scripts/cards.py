import random
from common import *

random.seed(21)
W, H = 400, 380
SX, SY, SW, SH = 16, 16, 368, 186   # scene viewport


def card(fname, idx, tag, tagc, title_a, title_b, stack, lines, scene, hud_l, hud_r):
    o = open_svg(W, H, f"{title_a} {title_b} — {stack}", aur=(0.5, 0.25, 0.7), corners=False)
    A = o.append
    o[2] = o[2].replace("</defs>", f'<clipPath id="sc"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="10"/></clipPath></defs>')
    A(f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="10" fill="#060608" stroke="{LINE}"/>')
    A(f'<g clip-path="url(#sc)">{scene}</g>')
    A(P(hud_l, "mono", 9.5, SX + 12, SY + 20, fill=DIM, ls=0.6))
    A(P(hud_r, "mono", 9.5, SX + SW - 12, SY + 20, fill=DIM, ls=0.6, anchor="end"))
    # text block
    A(P(idx, "mono", 11, 24, 232, fill=DIM, ls=1))
    tw = width(tag, "mono", 9.5, 1) + 16
    A(f'<rect x="{W - 24 - tw:.1f}" y="219" width="{tw:.1f}" height="18" rx="9" fill="{tagc}" fill-opacity="0.1" stroke="{tagc}" stroke-opacity="0.45"/>')
    A(P(tag, "mono", 9.5, W - 24 - tw + 8, 231.5, fill=tagc, ls=1))
    d, wa = path(title_a, "serif", 32, 24, 272, ls=-0.3)
    A(f'<path d="{d}" fill="{INK}"/>')
    d, _ = path(title_b, "serif-i", 32, 24 + wa + 9, 272, ls=-0.3)
    A(f'<path d="{d}" fill="url(#iv)"/>')
    A(P(stack, "mono", 10.5, 24, 296, fill=IND, ls=0.3))
    for i, ln in enumerate(lines):
        A(P(ln, "mono", 11.5, 24, 322 + i * 18, fill=MID))
    A(f'<path d="M24 358H{W - 24}" stroke="{LINE}"/>' if False else "")
    A(P("view repo ->", "mono-m", 10.5, W - 24, 364, fill=INK, ls=0.5, anchor="end"))
    save(o, fname)


# ---------------- ERP scene ----------------
s = []
cols, rows = 12, 5
gx, gy, cw, ch = SX + 24, SY + 48, 25, 23
lock = set(random.sample(range(cols * rows), 6))
for r in range(rows):
    for c in range(cols):
        x = gx + c * cw + (c // 4) * 14
        y = gy + r * ch
        i = r * cols + c
        s.append(f'<rect x="{x}" y="{y}" width="16" height="11" rx="1.5" fill="#18181b" stroke="#3f3f46" stroke-width="0.8"/>'
                 f'<path d="M{x + 8} {y + 11}v3M{x + 4} {y + 14.5}h8" stroke="#3f3f46" stroke-width="0.8"/>')
        delay = (c + r) * 0.07
        s.append(f'<rect x="{x + 1.5}" y="{y + 1.5}" width="13" height="8" rx="1" fill="{IND}" opacity="0.15">'
                 f'<animate attributeName="opacity" values="0.12;0.95;0.25;0.12" keyTimes="0;0.06;0.4;1" begin="{delay:.2f}s" dur="3s" repeatCount="indefinite"/></rect>')
        if i in lock:
            s.append(f'<rect x="{x + 1.5}" y="{y + 1.5}" width="13" height="8" rx="1" fill="{RED}" opacity="0">'
                     f'<animate attributeName="opacity" values="0;0;0.9;0.9;0" keyTimes="0;0.4;0.42;0.8;1" begin="{random.uniform(0, 3):.2f}s" dur="6s" repeatCount="indefinite"/></rect>')
for b in range(3):
    s.append(P(f"BRANCH 0{b + 1}", "mono", 8.5, gx + b * (4 * cw + 14), gy + rows * ch + 10, fill="#52525b", ls=1))
# hub pulse

card("card-erp.svg", "01 / C# · .NET", "REAL-TIME", LIME, "Gaming Café", "ERP",
     "C# · .NET 8 · React · SignalR · Redis · Docker",
     ["100+ PCs across branches, synced live.", "Remote lock / unlock agent per seat."],
     "".join(s), "signalr://hub · broadcast", "100+ nodes")

# ---------------- Prism learning studio scene ----------------
s = []
# An original page feeds an explanation, then a browser experiment.
s.append(f'<rect x="34" y="56" width="83" height="124" rx="5" fill="#111114" stroke="#3f3f46"/>')
s.append(P("PAPER", "mono", 8, 44, 72, fill=DIM, ls=1))
for i, w in enumerate([61, 54, 60, 42]):
    s.append(f'<rect x="44" y="{82+i*7}" width="{w}" height="2" rx="1" fill="#52525b"/>')
for i, h in enumerate([12, 24, 19, 31, 16]):
    s.append(f'<rect x="{44+i*12}" y="{149-h}" width="7" height="{h}" rx="1" fill="{VIO}" opacity=".7"/>')
s.append(P("ORIGINAL PAGE", "mono", 6.5, 43, 166, fill=DIM))
s.append(f'<rect x="30" y="77" width="91" height="2" fill="{LIME}" opacity=".7"><animate attributeName="y" values="77;154;77" dur="6s" repeatCount="indefinite"/></rect>')
s.append(f'<path d="M117 113H138V89H151M259 125V142" stroke="{IND}" stroke-opacity=".55" fill="none"/>')
s.append(f'<rect x="151" y="56" width="212" height="69" rx="6" fill="#101015" stroke="#34313f"/>')
s.append(P("LET\'S MAKE IT CLEAR", "mono", 8, 163, 73, fill=VIO, ls=.5))
for i,w in enumerate([179,166,125]):
    s.append(f'<rect x="163" y="{83+i*8}" width="{w}" height="2.5" rx="1" fill="#71717a"><animate attributeName="opacity" values=".3;.85;.3" dur="5s" begin="{i*.3}s" repeatCount="indefinite"/></rect>')
s.append(f'<rect x="151" y="142" width="212" height="43" rx="6" fill="#0e1210" stroke="{LIME}" stroke-opacity=".3"/>')
s.append(P("TRY THE IDEA", "mono", 7.5, 162, 157, fill=LIME, ls=.5))
s.append(P("5 LABS", "mono", 7, 351, 157, fill=DIM, anchor="end"))
for i,h in enumerate([3,7,5,15,10,8,12,6]):
    s.append(f'<rect x="{163+i*23}" y="{177-h}" width="16" height="{h}" rx="1" fill="{LIME}" opacity=".6"/>')
s.append(f'<circle r="2.7" fill="{VIO}"><animateMotion path="M117 113H138V89H151" dur="3s" repeatCount="indefinite"/></circle>')
s.append(f'<circle r="2.5" fill="{LIME}"><animateMotion path="M259 125V142" dur="3s" repeatCount="indefinite"/></circle>')
card("card-prism.svg", "02 / PYTHON", "PAPER STUDIO", VIO, "Prism", "Studio",
     "FastAPI · Gemini · SQLite · JavaScript",
     ["Your papers. Clearer explanations.", "Saved chats, sources + 5 learning labs."],
     "".join(s), "pdf -> understand -> experiment", "prism")

# ---------------- CCTV scene ----------------
s = []
# floor perspective
hx = SX + SW / 2
for i in range(-6, 7):
    s.append(f'<path d="M{hx + i * 8} {SY + 70}L{hx + i * 70} {SY + SH}" stroke="#18181b"/>')
for j, yy in enumerate([90, 112, 140, 176]):
    s.append(f'<path d="M{SX} {SY + yy}H{SX + SW}" stroke="#18181b"/>')

def worker(x, y, sc, hat, vest, label, ok, dx, dur):
    g = [f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{dx} 0;0 0" dur="{dur}s" repeatCount="indefinite"/>',
         f'<g transform="translate({x} {y}) scale({sc})">']
    g.append(f'<circle cx="0" cy="-58" r="9" fill="#3f3f46"/>')
    g.append(f'<rect x="-13" y="-46" width="26" height="36" rx="7" fill="{"#a16207" if vest else "#3f3f46"}"/>')
    if vest:
        g.append(f'<path d="M-13 -30h26" stroke="#fde047" stroke-width="3"/>')
    g.append(f'<rect x="-11" y="-12" width="9" height="30" rx="4" fill="#3f3f46"/><rect x="2" y="-12" width="9" height="30" rx="4" fill="#3f3f46"/>')
    if hat:
        g.append(f'<path d="M-11 -61a11 9 0 0 1 22 0z" fill="#facc15"/><path d="M-13 -61h26" stroke="#facc15" stroke-width="2"/>')
    col = LIME if ok else RED
    g.append(f'<rect x="-24" y="-74" width="48" height="96" fill="none" stroke="{col}" stroke-width="{1.6 / sc:.2f}"/>')
    lw = width(label, "mono-b", 8.5) + 8
    g.append(f'<g transform="scale({1 / sc:.3f})"><rect x="{-24 * sc - 0.8:.1f}" y="{-74 * sc - 13:.1f}" width="{lw:.1f}" height="13" fill="{col}"/>'
             + P(label, "mono-b", 8.5, -24 * sc + 3.2, -74 * sc - 3.5, fill="#09090b") + '</g>')
    if not ok:
        g.insert(2, f'<animate attributeName="opacity" values="1;0.35;1" dur="0.6s" repeatCount="indefinite"/>')
    g.append('</g></g>')
    return "".join(g)

s.append(worker(SX + 80, SY + 150, 0.85, True, True, "ppe_ok 0.96", True, 14, 5))
s.append(worker(SX + 290, SY + 164, 1.0, True, True, "hardhat 0.93", True, -18, 6))
s.append(worker(SX + 192, SY + 128, 0.68, False, False, "no_hardhat 0.88", False, 10, 4))
# alert banner
s.append(f'<g><animate attributeName="opacity" values="1;0.2;1" dur="0.6s" repeatCount="indefinite"/>'
         f'<rect x="{SX + SW / 2 - 57}" y="{SY + 30}" width="114" height="16" rx="3" fill="{RED}" fill-opacity="0.15" stroke="{RED}"/>'
         + P("ALERT · ZONE B", "mono-b", 8.5, SX + SW / 2, SY + 41.5, fill=RED, anchor="middle", ls=1) + '</g>')
s.append(f'<rect x="{SX}" y="{SY}" width="{SW}" height="3" fill="{LIME}" opacity="0.12"><animate attributeName="y" values="{SY};{SY + SH}" dur="2.6s" repeatCount="indefinite"/></rect>')
card("card-cctv.svg", "03 / VISION", "LIVE WEBRTC", RED, "AI CCTV", "Safety",
     "YOLOv8 · PyTorch · OpenCV · Streamlit",
     ["Live PPE detection — hard hats, vests,", "masks — with instant alerts."],
     "".join(s), "REC · CAM_03 · yolov8", "30 fps")
print("ok")