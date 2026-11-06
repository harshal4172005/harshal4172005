"""Build the profile's original vector illustrations. Run locally with fonttools.

Lettering is outlined so SVG image rendering never needs remote fonts.
The activity renderer is separate and uses only Python's standard library.
"""
import math
from pathlib import Path
from html import escape
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
INK = '#101319'
PAPER = '#eeeae0'
MUTED = '#92999e'
LINE = '#343b42'
LIME = '#d4fc67'
BLUE = '#a9baff'
fonts = {key: TTFont('C:/Windows/Fonts/' + file) for key, file in
         [('bold', 'ariblk.ttf'), ('serif', 'georgiai.ttf'), ('mono', 'consola.ttf')]}

def text(s, x, y, size=14, color=PAPER, font='mono', spacing=0):
    f = fonts[font]
    glyphs, cmap, scale = f.getGlyphSet(), f.getBestCmap(), size / f['head'].unitsPerEm
    parts = []
    for c in s:
        name = cmap.get(ord(c), '.notdef')
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        parts.append(f'<path d="{pen.getCommands()}" transform="translate({x:.3f} {y}) scale({scale} {-scale})"/>')
        x += glyphs[name].width * scale + spacing
    return f'<g fill="{color}" aria-label="{escape(s, quote=True)}">' + ''.join(parts) + '</g>'

def line(x1,y1,x2,y2,color=LINE):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{color}"/>' if y1 == y2 else f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}"/>'

def rect(x,y,w,h,fill=INK,stroke=LINE,rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'

def svg(name, height, content, title, bg=INK):
    head=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-label="{escape(title, quote=True)}"><title>{escape(title)}</title>
    <style>@keyframes dash{{to{{stroke-dashoffset:-120}}}} @keyframes breathe{{50%{{opacity:.25}}}} .flow{{stroke-dasharray:6 14;animation:dash 12s linear infinite}} .pulse{{animation:breathe 3s ease-in-out infinite}} @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
    <rect width="1200" height="{height}" fill="{bg}"/>'''
    (ASSETS/name).write_text(head+content+'</svg>',encoding='utf-8')

def section(n,title,tag):
    return text(n,32,43,13,LIME)+text(title,77,45,24,PAPER,'bold')+text(tag,820,42,12,MUTED)+line(32,65,1168,65)

def hero():
    c=text('HP / ENGINEERING FIELDNOTES',32,38,13,LIME,spacing=1.1)
    c+=text('SURAT, IN  /  OPEN TO WORK',853,38,13,PAPER)
    c+=line(32,57,1168,57)
    c+=text('HARSHAL',28,176,104,PAPER,'bold')+text('PAREKH',28,280,104,PAPER,'bold')
    c+=text('AI ENGINEER / SYSTEMS DEVELOPER',35,323,16,LIME)
    c+=text('I turn models into',33,385,38,PAPER,'serif')
    c+=text('systems people use.',33,430,38,PAPER,'serif')
    # A continuous signal bends through three stages: noise -> inference -> output.
    c+=rect(704,81,464,356,'#151a20',LINE)
    for j in range(38):
        pts=[]
        for k in range(101):
            t=k/100
            x=722+t*430
            envelope=math.sin(t*math.pi)**1.3
            y=255+(j-18.5)*5 + envelope*(64*math.sin(t*7+j*.10)+18*math.cos(t*19+j*.21))
            pts.append(f'{x:.1f},{y:.1f}')
        color=LIME if j%9==0 else BLUE
        c+=f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="{1.5 if j%9==0 else .7}" opacity="{.9 if j%9==0 else .28}"/>'
        if j%9==0:
            c+=f'<circle r="2.7" fill="{LIME}"><animateMotion dur="{6+j*.06}s" repeatCount="indefinite" path="M'+ ' L'.join(p.replace(',', ' ') for p in pts)+'"/></circle>'
    c+=text('01 / LATENT SPACE',724,108,12,MUTED)
    c+=text('x(t) -> inference -> y',724,411,14,LIME)
    c+=line(32,467,1168,467)
    c+=text('DIFFUSION',33,499,12,PAPER)+text('COMPUTER VISION',230,499,12,PAPER)+text('MULTIMODAL RAG',490,499,12,PAPER)
    c+=text('IDEA  ->  API  ->  PRODUCTION',826,499,12,LIME)
    svg('hero-header.svg',526,c,'Harshal Parekh. AI engineer and systems developer. I turn models into systems people use.')

def about():
    c=section('01','THE ENGINEER','PROFILE / EXPERIENCE + EDUCATION')
    rows=[('FOCUS','Production AI, vision & backend systems'),('EXPERIENCE','Diffusion image + video pipelines / NexAI Labs'),('DEPLOYMENT','FastAPI / Docker / AWS EC2 / S3 / Cloudflare R2'),('EDUCATION','B.E. Computer Engineering / CGPA 8.41'),('BASE','Surat, India / open to roles worldwide')]
    for i,(a,b) in enumerate(rows):
        y=110+i*43
        c+=text(a,32,y,12,MUTED)+text(b,245,y,16,PAPER)+line(245,y+16,1168,y+16)
    c+=text('5+',33,365,42,LIME,'bold')+text('commercial brands',114,359,14,PAPER)
    c+=text('60%',430,365,42,LIME,'bold')+text('faster turnaround',562,359,14,PAPER)
    c+=text('100+',848,365,42,LIME,'bold')+text('PCs / ERP',1010,359,14,PAPER)
    c+=text('Experience and impact figures supplied by Harshal; activity below is fetched from GitHub.',33,403,11,MUTED)
    svg('model-card.svg',430,c,'Engineering background: NexAI Labs production diffusion, BE Computer Engineering CGPA 8.41, Surat India.')

def architecture():
    c=section('02','FROM PROMPT TO PRODUCTION','NEXAI LABS / SYSTEM MAP')
    nodes=[(32,173,'INPUT','Prompt / media'),(265,107,'ORCHESTRATE','n8n / multi-agent'),(265,254,'SERVE','FastAPI'),(566,107,'GENERATE','Diffusion / image'),(566,254,'GENERATE','Video pipeline'),(884,107,'STORE','Amazon S3'),(884,254,'DELIVER','Cloudflare R2')]
    paths=['M212 209C244 209 230 143 265 143','M212 209C244 209 230 290 265 290','M501 143H566','M501 290H566','M802 143H884','M802 290H884','M383 179V254','M684 179V254']
    for i,p in enumerate(paths):
        c+=f'<path d="{p}" fill="none" stroke="{LINE}" stroke-width="2"/><path d="{p}" fill="none" stroke="{LIME if i%2==0 else BLUE}" class="flow"/>'
    for x,y,a,b in nodes:
        w=180 if x==32 else 236 if x<884 else 284
        c+=rect(x,y,w,72,'#181e24')+text(a,x+16,y+25,11,LIME)+text(b,x+16,y+51,16,PAPER)
    c+=text('RUNTIME',32,374,12,MUTED)+text('Docker containers / AWS EC2',180,374,15,PAPER)
    c+=text('OUTPUT',700,374,12,MUTED)+text('Garment + jewelry assets',813,374,15,PAPER)
    svg('production-map.svg',410,c,'NexAI production pipeline: prompt to n8n and FastAPI, diffusion and video generation, S3 and Cloudflare R2.')

def stack():
    c=section('03','TOOLS, CONNECTED','THE STACK / TOOLCHAIN')
    columns=[('WRITE',['Python','C# / .NET 8','JavaScript','SQL']),('INFER',['PyTorch / TensorFlow','YOLOv8 / OpenCV','Diffusion','LangChain / Gemini']),('SERVE',['FastAPI / Flask','React / SignalR','PostgreSQL / Redis','Qdrant']),('SHIP',['Docker / Linux','AWS EC2 / S3','Google Cloud','Cloudflare R2 / n8n'])]
    for i,(title,items) in enumerate(columns):
        x=32+i*292
        c+=text(title,x,109,12,LIME)+text(f'0{i+1}',x+236,109,12,MUTED)
        for j,item in enumerate(items):
            c+=text(item,x,150+j*38,15,PAPER)
        c+=line(x,289,x+260,289,LIME)
    svg('stack-map.svg',318,c,'Technology stack: languages, machine learning, backend data and deployment tools.')

def projects():
    projects=[('project-erp.svg','01 / DISTRIBUTED SYSTEMS','Gaming Cafe','ERP','100+ PCs. Multiple branches. One state.','C# / .NET 8 / React / SignalR / Redis'),('project-rag.svg','02 / MULTIMODAL RETRIEVAL','Research','without blind spots.','Papers, figures and context in one retrieval flow.','Python / LangChain / Gemini / Qdrant'),('project-vision.svg','03 / REAL-TIME VISION','Safety,','frame by frame.','Live PPE detection with alerts and audit trails.','YOLOv8 / PyTorch / OpenCV / Streamlit')]
    for idx,(file,tag,a,b,desc,tech) in enumerate(projects):
        c=text(tag,33,38,12,LIME)+line(32,59,1168,59)
        c+=text(a,32,135,51,PAPER,'bold')+text(b,32,199,51,PAPER,'bold')
        c+=text(desc,34,250,15,PAPER)+text(tech,34,281,12,MUTED)
        c+=text('OPEN THE REPOSITORY  ->',34,334,13,LIME)
        c+=rect(760,82,407,259,'#181e24')
        if idx==0:
            for j in range(45):
                x=789+(j%9)*40;y=119+(j//9)*39
                c+=rect(x,y,25,17,'#242f36','#53616c',2)+line(x+7,y+21,x+18,y+21)
                if j%4==0:c+=f'<rect x="{x+3}" y="{y+3}" width="19" height="11" fill="{LIME}" class="pulse" style="animation-delay:-{j/10}s"/>'
            c+=text('STATE SYNC / SIGNALR',788,321,12,LIME)
        elif idx==1:
            c+=rect(785,107,102,174,'#101319',LINE)
            for j in range(9):c+=line(800,125+j*15,866-(j%3)*8,125+j*15,'#687581')
            for j in range(29):
                x=943+(j*37%180);y=126+(j*53%135)
                c+=f'<circle cx="{x}" cy="{y}" r="3" fill="{BLUE}"/>'
            c+='<path d="M887 194H1010L1078 163M1010 194L1090 240" fill="none" stroke="'+LIME+'" class="flow"/>'
            c+=text('DOCUMENT -> VECTORS -> CONTEXT',788,321,12,LIME)
        else:
            for j in range(3):
                x=791+j*115
                color=LIME if j!=1 else '#ff856a'
                c+=f'<circle cx="{x+30}" cy="156" r="14" fill="#687581"/><path d="M{x+30} 180V229M{x+12} 195H{x+48}M{x+30} 229L{x+14} 264M{x+30} 229L{x+46} 264" stroke="#687581" stroke-width="14" stroke-linecap="round"/>'
                c+=rect(x,127,63,153,'none',color)+text('PPE' if j!=1 else 'ALERT',x+3,119,11,color)
            c+=f'<path d="M780 186H1150" stroke="{LIME}" opacity=".5"><animateTransform attributeName="transform" type="translate" values="0 -55;0 85;0 -55" dur="5s" repeatCount="indefinite"/></path>'
            c+=text('DETECT / TRACK / ALERT',788,321,12,LIME)
        svg(file,366,c,tag+': '+a+' '+b+'. '+desc)

def footer():
    c=text('END OF FILE / START OF A CONVERSATION',33,38,12,INK)
    c+=line(32,60,1168,60,'#95af4b')
    c+=text("LET'S BUILD",28,164,91,INK,'bold')+text('something that ships.',33,229,50,INK,'serif')
    c+=text('AI / ML / BACKEND ENGINEERING',35,291,14,INK)
    c+=text('harshalparekh17@gmail.com  ->',768,291,16,INK)
    c+=f'<path d="M1040 105H1145V210M1145 105L1038 212" fill="none" stroke="{INK}" stroke-width="5"/>'
    svg('dispatch-bar.svg',325,c,'Let us build something that ships. Email harshalparekh17@gmail.com. Open to AI ML and backend engineering roles.',LIME)

if __name__=='__main__':
    hero(); about(); architecture(); stack(); projects(); footer()
    print('Built eight original SVG illustrations.')
