"""Readable GitHub-width graphics and naturally wrapping project layouts.

Primary content is also normal Markdown in README for accessible mobile reading.
"""
import math
import runpy
import textwrap
import xml.etree.ElementTree as ET
import common
from common import *
MID='#c3c5ce'; DIM='#a0a2b0'

PROJECTS=[('erp','Gaming Cafe','ERP','01 / DISTRIBUTED SYSTEMS',LIME,'C# · .NET 8 · React · SignalR · Redis · Docker','100+ PCs across branches, synced live. Remote lock / unlock agent per seat.'),
('rag','Multimodal','RAG','02 / MULTIMODAL RETRIEVAL',VIO,'Python · LangChain · FastAPI · Gemini · Qdrant','Research-paper QA that reads the figures. Gemini Vision captions and Qdrant retrieval.'),
('cctv','AI CCTV','Safety','03 / REAL-TIME VISION',RED,'YOLOv8 · PyTorch · OpenCV · Streamlit','Live PPE detection for hard hats, vests and masks, with instant alerts and audit logs.')]

def section(num,title):
    o=open_svg(840,76,title,corners=False)
    o+=[P(num,'serif-i',40,26,51,fill=VIO),P(title,'serif',40,80,51,fill=INK)]
    save(o,'readable-sec-'+num+'.svg')

def ascent(w=840,mobile=False):
    h=386 if mobile else 410
    o=open_svg(w,h,'Capability ascent: Python to APIs, computer vision, generative AI and production. Illustrative growth.')
    A=o.append
    A(P('CAPABILITY ASCENT','mono-b',16 if mobile else 20,28,47,fill=VIO))
    left,right=36,w-36;bottom,top=280 if mobile else 300,100
    def route(phase=None):
        pts=[]
        for i in range(101):
            t=i/100;x=left+(right-left)*t;y=bottom-(bottom-top)*t**.95
            if phase is not None:y+=15*math.sin(math.pi*t)*math.sin(t*11+phase)
            pts.append((x,y))
        return 'M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in pts)
    o[2]=o[2].replace('</defs>','<linearGradient id="fill" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#a78bfa" stop-opacity=".15"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/></linearGradient></defs>')
    main=route()
    for y in [140,200,260,320]:A(f'<path d="M{left} {y}H{right}" stroke="{LINE}" stroke-dasharray="2 7"/>')
    A(f'<path d="{main}L{right} {bottom+12}H{left}Z" fill="url(#fill)"/>')
    for j,(phase,col) in enumerate([(0,IND),(2.1,VIO),(4.2,CYAN)]):
        d=route(phase);A(f'<path d="{d}" fill="none" stroke="{col}" opacity=".65"/>')
        for k in range(2):A(f'<circle r="3" fill="{col}"><animateMotion path="{d}" begin="{-j-k*3}s" dur="6s" repeatCount="indefinite"/></circle>')
    A(f'<path d="{main}" fill="none" stroke="{VIO}" stroke-width="2.5"/>')
    for i,label in enumerate(['Python','APIs','Vision','GenAI','Production']):
        t=i/4;x=left+(right-left)*t;y=bottom-(bottom-top)*t**.95
        A(f'<path d="M{x} {y+10}V{bottom+24}" stroke="{IND}" opacity=".25" stroke-dasharray="2 5"/><circle cx="{x}" cy="{y}" r="5" fill="{BG}" stroke="{VIO}" stroke-width="2"/>')
        label=['PY','APIs','Vision','GenAI','Prod'][i] if mobile else label
        A(P(label,'mono',14 if mobile else 18,x,bottom+54,fill=MID,anchor='start' if i==0 else 'end' if i==4 else 'middle'))
        if i in [1,2,3]:A(f'<g transform="translate({x} {y})"><circle r="14" fill="none" stroke="{VIO}" stroke-dasharray="2 5" opacity=".3"/><g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="{8+i}s" repeatCount="indefinite"/><circle cx="14" r="2" fill="{CYAN}"/></g></g>')
    A(f'<circle cx="{right}" cy="{top}" r="5" fill="{LIME}"/><circle cx="{right}" cy="{top}" r="8" fill="none" stroke="{LIME}"><animate attributeName="r" values="7;18;7" dur="3s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0;.7" dur="3s" repeatCount="indefinite"/></circle>')
    A(P('Learning compounds with every build.','mono',13 if mobile else 17,28,h-25,fill=VIO))
    save(o,'readable-ascent-mobile.svg' if mobile else 'readable-ascent.svg')

def stack():
    o=open_svg(840,494,'Connected toolchain: languages, ML and vision, backend and data, cloud infrastructure.')
    A=o.append
    cols=[(28,182,'LANGUAGES',AMB,['Python','C#','JavaScript','SQL']),
          (234,120,'ML / VISION',VIO,['PyTorch','TensorFlow','YOLOv8','OpenCV','Diffusion','LangChain','Gemini']),
          (440,100,'SERVE / DATA',IND,['FastAPI','Flask','.NET 8','React','SignalR','Redis','PostgreSQL','Qdrant']),
          (646,140,'INFRA / CLOUD',CYAN,['Docker','AWS','GCP','Cloudflare R2','n8n','Linux'])]
    pw=166;paths=[]
    for n in range(3):
        x,y,_,col,items=cols[n];nx,ny,_,_,nextitems=cols[n+1]
        for i in range(len(items)):
            for j in range(len(nextitems)):
                sy=y+i*42+17;ey=ny+j*42+17
                d=f'M{x+pw} {sy}C{x+pw+22} {sy} {nx-22} {ey} {nx} {ey}'
                A(f'<path d="{d}" fill="none" stroke="#44404f" opacity=".3"/>');paths.append((d,col))
    for x,y,title,col,items in cols:
        A(P(title,'mono-b',15,x,57,fill=col))
        for i,item in enumerate(items):
            yy=y+i*42
            A(f'<rect x="{x}" y="{yy}" width="166" height="34" rx="7" fill="#101015" stroke="{col}" stroke-opacity=".45"/>')
            A(P(item,'mono',17,x+12,yy+23,fill=INK))
    for k in range(18):
        d,col=paths[(17*k)%len(paths)]
        A(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="24 800"><animate attributeName="stroke-dashoffset" values="40;-800" begin="{k*.3}s" dur="4s" repeatCount="indefinite"/></path>')
    A(P('Idea -> model -> service -> production','mono',18,28,466,fill=MID))
    save(o,'readable-forward-pass.svg')

def architecture():
    o=open_svg(840,582,'NexAI production: n8n orchestration and FastAPI, diffusion and video, S3 and R2. Docker on EC2.')
    A=o.append;A(P('NEXAI LABS / PRODUCTION','mono-b',21,28,49,fill=IND))
    A(P('Docker on AWS EC2','mono',17,28,80,fill=MID))
    nodes={'client':(28,227,150,'CLIENT','Prompt / media',AMB),'router':(222,137,174,'n8n ROUTER','Multi-agent',VIO),'api':(222,297,174,'FASTAPI','Microservice',IND),'diff':(432,137,174,'DIFFUSION','Image pipeline',VIO),'video':(432,297,174,'VIDEO GEN','Video pipeline',IND),'s3':(642,137,170,'AWS S3','Asset store',CYAN),'r2':(642,297,170,'CLOUDFLARE R2','Delivery',CYAN)}
    routes=[]
    for a,b in [('client','router'),('router','diff'),('api','video'),('diff','s3'),('video','r2')]:
        x,y,w,*_=nodes[a];xx,yy,*_=nodes[b]
        routes.append((f'M{x+w} {y+43}C{x+w+22} {y+43} {xx-22} {yy+43} {xx} {yy+43}',LIME if a=='client' else VIO))
    routes.extend([('M309 223V297',IND),('M519 223V297',VIO)])
    for d,c in routes:A(f'<path d="{d}" fill="none" stroke="#52525b" stroke-width="1.5"/>')
    for x,y,w,title,sub,col in nodes.values():
        A(f'<rect x="{x}" y="{y}" width="{w}" height="86" rx="10" fill="#101015" stroke="{LINE}"/><path d="M{x+12} {y}h36" stroke="{col}" stroke-width="2"/>')
        A(P(title,'mono-b',16 if len(title)>10 else 18,x+12,y+34,fill=INK))
        A(P(sub,'mono',16,x+12,y+62,fill=MID))
    for i,(d,col) in enumerate(routes):
        A(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="26 800"><animate attributeName="stroke-dashoffset" values="30;-800" begin="{i*.4}s" dur="5s" repeatCount="indefinite"/></path><circle r="3" fill="{col}"><animateMotion path="{d}" begin="{-i}s" dur="5s" repeatCount="indefinite"/></circle>')
    A('<path d="M28 435H812" stroke="#27272a"/>')
    for x,val,label in [(28,'5+','commercial brands'),(306,'60%','faster turnaround'),(584,'2','image + video flows')]:
        A(P(val,'mono-b',40,x,498,fill=VIO));A(P(label,'mono',17,x,537,fill=MID))
    save(o,'readable-inference-graph.svg')

def projects():
    # Reuse the original animations without writing or changing legacy cards.
    captured={};original=common.save
    def capture(o,name):captured[name]=''.join(o+['</svg>'])
    common.save=capture
    try:runpy.run_path(str(ROOT/'scripts/cards.py'))
    finally:common.save=original
    ET.register_namespace('','http://www.w3.org/2000/svg')
    for key,a,b,tag,col,tools,desc in PROJECTS:
        scene=next(e for e in ET.fromstring(captured['card-'+key+'.svg']) if e.get('clip-path')=='url(#sc)')
        scene=ET.tostring(scene,encoding='unicode')
        for mobile in [False,True]:
            w,h=(400,530) if mobile else (840,320)
            o=open_svg(w,h,a+' '+b+': '+desc,corners=False);A=o.append
            o[2]=o[2].replace('</defs>','<clipPath id="sc"><rect x="16" y="16" width="368" height="186" rx="10"/></clipPath></defs>')
            A(f'<g transform="translate({0 if mobile else 8} {12 if mobile else 44})"><rect x="16" y="16" width="368" height="186" rx="10" fill="#060608" stroke="{LINE}"/>{scene}</g>')
            tx,ty=(24,270) if mobile else (424,87)
            if not mobile:A(P(tag,'mono-b',14,24,32,fill=col))
            A(P(a,'serif',40 if mobile else 46,tx,ty,fill=INK))
            xa=tx+width(a,'serif',40 if mobile else 46)+12
            A(P(b,'serif-i',40 if mobile else 46,xa,ty,fill=VIO))
            y=ty+34
            for ln in textwrap.wrap(tools,34):
                A(P(ln,'mono',15 if mobile else 16,tx,y,fill=IND));y+=23
            y+=14
            for ln in textwrap.wrap(desc,33 if mobile else 36):
                A(P(ln,'mono',17,tx,y,fill=MID));y+=25
            A(P('Open repository ->','mono-b',18,tx,h-27,fill=col))
            save(o,'readable-project-'+key+('-mobile' if mobile else '')+'.svg')

def contacts():
    for key,title,sub,col in [('email','Email','',LIME),('linkedin','LinkedIn','',VIO),('resume','Resume','',IND),('source','Source code','',CYAN)]:
        o=open_svg(280,76,title,corners=False)
        o.append(P(title,'mono-b',24,24,47,fill=INK))
        o.append(f'<path d="M244 26h12v12M256 26l-14 14" fill="none" stroke="{col}" stroke-width="2"/>')
        o.append(f'<path d="M24 75H256" stroke="{col}" opacity=".55"/>')
        save(o,'readable-contact-'+key+'.svg')

def footer():
    o=open_svg(840,252,'Available for AI, ML and backend engineering. Email harshalparekh17@gmail.com.')
    o.append(P('AVAILABLE FOR AI / ML / BACKEND','mono',17,28,44,fill=LIME))
    command='Engineer().hire(role="AI/ML", where="worldwide")'
    tw=width(command,'mono',18)
    o[2]=o[2].replace('</defs>',f'<clipPath id="type"><rect x="28" y="63" width="{tw}" height="30"><animate attributeName="width" values="0;0;{tw};{tw}" keyTimes="0;.1;.6;1" dur="9s" repeatCount="indefinite"/></rect></clipPath></defs>')
    o.append('<g clip-path="url(#type)">'+P(command,'mono',18,28,87,fill=MID)+'</g>')
    o.append(P("Let's ship it.",'serif',68,28,170,fill=INK))
    o.append(P('Surat, India / Remote worldwide','mono',17,28,219,fill=MID))
    o.append(P('harshalparekh17@gmail.com','mono',17,812,219,fill=VIO,anchor='end'))
    save(o,'readable-dispatch.svg')

def main():
    for n,title in [('01','The engineer'),('02','Forward pass'),('03','Production architecture'),('04','Selected builds'),('05','Live GitHub activity')]:section(n,title)
    ascent();ascent(400,True);stack();architecture();projects();contacts();footer()
    print('Built readable desktop/mobile illustrations.')

if __name__=='__main__':main()
