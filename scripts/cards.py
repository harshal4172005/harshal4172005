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

# ---------------- RAG scene ----------------
s = []
px, py = SX + 26, SY + 36
s.append(f'<rect x="{px}" y="{py}" width="96" height="128" rx="4" fill="#111114" stroke="#3f3f46"/>')
for i in range(5):
    s.append(f'<rect x="{px + 10}" y="{py + 12 + i * 8}" width="{random.randint(48, 76)}" height="3" rx="1.5" fill="#3f3f46"/>')
# figure
fx, fy = px + 10, py + 58
s.append(f'<rect x="{fx}" y="{fy}" width="76" height="40" rx="2" fill="none" stroke="{VIO}" stroke-opacity="0.7" stroke-dasharray="2 2"/>')
for i, hgt in enumerate([14, 24, 18, 30, 22]):
    s.append(f'<rect x="{fx + 8 + i * 13}" y="{fy + 36 - hgt}" width="8" height="{hgt}" fill="{VIO}" opacity="0.7"/>')
s.append(P("fig.3", "mono", 7.5, fx + 2, fy - 3, fill=VIO))
for i in range(3):
    s.append(f'<rect x="{px + 10}" y="{py + 106 + i * 7}" width="{random.randint(40, 76)}" height="3" rx="1.5" fill="#3f3f46"/>')
s.append(f'<rect x="{px - 4}" y="{py}" width="104" height="2" fill="{LIME}" opacity="0.8" filter="url(#glow)">'
         f'<animate attributeName="y" values="{py};{py + 126};{py}" dur="3s" repeatCount="indefinite"/></rect>')
# vector space
vx, vy, vw, vh = SX + 200, SY + 38, 150, 128
s.append(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="6" fill="none" stroke="#27272a" stroke-dasharray="2 4"/>')
pts = [(vx + random.uniform(10, vw - 10), vy + random.uniform(10, vh - 10)) for _ in range(34)]
q = (vx + 92, vy + 60)
near = sorted(range(len(pts)), key=lambda i: (pts[i][0] - q[0]) ** 2 + (pts[i][1] - q[1]) ** 2)[:3]
for i, (x, y) in enumerate(pts):
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="{IND}" opacity="0.55"/>')
for i in near:
    x, y = pts[i]
    s.append(f'<path d="M{q[0]} {q[1]}L{x:.1f} {y:.1f}" stroke="{LIME}" stroke-width="1" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.55;0.62;0.92;1" dur="4s" repeatCount="indefinite"/></path>')
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{LIME}" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.6;0.65;0.92;1" dur="4s" repeatCount="indefinite"/></circle>')
s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.45;0.5;0.92;1" dur="4s" repeatCount="indefinite"/>'
         f'<path d="M{q[0]} {q[1] - 6}l1.8 4.2 4.2 1.8-4.2 1.8-1.8 4.2-1.8-4.2-4.2-1.8 4.2-1.8z" fill="{AMB}"/>'
         + P("query", "mono", 8, q[0] + 8, q[1] - 6, fill=AMB) + '</g>')
s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.7;0.75;0.92;1" dur="4s" repeatCount="indefinite"/>'
         + P("top_k=3 -> answer", "mono", 8.5, vx + vw - 4, vy + vh + 12, fill=LIME, anchor="end") + '</g>')
# chunks flying page -> space
for k in range(5):
    tgt = pts[k * 5]
    s.append(f'<rect width="10" height="6" rx="1" fill="{VIO}" opacity="0">'
             f'<animateMotion path="M{px + 96} {py + 30 + k * 18}C{px + 150} {py + 30 + k * 18} {tgt[0] - 40:.0f} {tgt[1]:.0f} {tgt[0]:.0f} {tgt[1]:.0f}" dur="4s" begin="{k * 0.18:.2f}s" repeatCount="indefinite" keyPoints="0;0;1;1" keyTimes="0;0.05;0.35;1" calcMode="linear"/>'
             f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.05;0.33;0.36;1" dur="4s" begin="{k * 0.18:.2f}s" repeatCount="indefinite"/></rect>')
card("card-rag.svg", "02 / PYTHON", "MULTIMODAL", VIO, "Multimodal", "RAG",
     "LangChain · FastAPI · Gemini · Qdrant",
     ["Research-paper QA that reads the figures.", "Gemini Vision captions + Groq/NVIDIA chain."],
     "".join(s), "pdf -> chunks -> qdrant", "gemini-vision")

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