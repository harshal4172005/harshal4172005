"""Section bars and the engineering model card, matching the supplied references."""
import math
import random
from common import *
random.seed(17)

def heading(num,name,code,sub):
    o=open_svg(1200,70,f'{num} {name}: {sub}',corners=False)
    A=o.append
    A(P(num,'serif-i',40,28,47,fill=VIO))
    x=28+width(num,'serif-i',40)+16
    A(P(name,'serif',40,x,47,fill=INK))
    x+=width(name,'serif',40)+23
    A(P('// '+code,'mono',12,x,44,fill=DIM,ls=.5))
    x+=width('// '+code,'mono',12,.5)+24
    xe=1172-width(sub.upper(),'mono',10,1.2)-26
    A(f'<path d="M{x} 40H{xe}" stroke="#27272a"/>')
    A(f'<circle cx="{x}" cy="40" r="2.5" fill="{IND}"><animate attributeName="cx" values="{x};{xe};{x}" dur="10s" repeatCount="indefinite"/></circle>')
    A(P(sub.upper(),'mono',10,1172,44,fill=DIM,ls=1.2,anchor='end'))
    save(o,f'sec-{num}.svg')

def model_card():
    o=open_svg(1200,460,'Harshal Parekh model card: AI engineering background and an illustrative rising learning curve from Python foundations to production AI systems.')
    A=o.append
    A(P('MODEL CARD','mono-b',11,44,50,fill=IND,ls=1.8))
    A(segs([('harshal-parekh/',INK),('v2026.11',VIO)],150,50,'mono-m',13)[0])
    x=758
    for label,color in [('ai-engineer',IND),('diffusion',VIO),('vision',LIME),('rag',CYAN),('open-to-work',LIME)]:
        tw=width(label,'mono',10,0.5)+18
        A(f'<rect x="{x}" y="35" width="{tw}" height="21" rx="10.5" fill="{color}" fill-opacity=".07" stroke="{color}" stroke-opacity=".35"/>')
        A(P(label,'mono',10,x+9,49,fill=color,ls=.5));x+=tw+8
    A('<path d="M44 72H1156" stroke="#27272a"/>')
    rows=[(112,'architecture',[('AI engineer × systems developer',INK)]),
          (151,'pretrained on',[('B.E. Computer Engineering',INK),(' — C.K. Pithawala College',MID),('  CGPA 8.41',AMB)]),
          (190,'fine-tuned on',[('NexAI Labs',INK),(' — production diffusion',MID)]),
          (216,'',[('image + video pipelines for ',MID),('5+ garment & jewelry brands',INK)]),
          (255,'serving',[('AWS EC2 · FastAPI · Docker · Cloudflare R2',INK)]),
          (294,'side quests',[('multi-agent n8n · real-time ERP · multimodal RAG',INK)]),
          (333,'skill badges',[('Google Cloud',INK),(' — 22 badges (Gemini, Cloud Run, Vision)',MID)]),
          (372,'availability',[('open to full-time roles · worldwide · available now',LIME)])]
    for y,label,items in rows:
        if label:A(P(label,'mono',12,44,y,fill=DIM,ls=.4))
        A(segs(items,196,y,'mono',12)[0])
    A(segs([('from ',VIO),('transformers ',INK),('import ',VIO),('pipeline ',IND),(' # just kidding, it is a person.',DIM)],44,418,'mono',11.5)[0])
    A('<rect x="750" y="80" width="420" height="332" rx="12" fill="#0d0d12" stroke="#27272a"/>')
    A(P('LEARNING CURVE · capabilities in practice','mono',9.5,770,101,fill=DIM,ls=.2))
    A('<defs><linearGradient id="growth-fill" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#a78bfa" stop-opacity=".15"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/></linearGradient></defs>')
    milestones=[(780,337,'Python'),(868,292,'APIs'),(958,246,'Vision'),(1052,192,'GenAI'),(1147,138,'Production')]
    d='M780 337C810 331 839 307 868 292S927 265 958 246S1020 215 1052 192S1119 155 1147 138'
    for yy in [160,220,280,340]:
        A(f'<path d="M770 {yy}H1150" stroke="#27272a" stroke-dasharray="2 6" opacity=".45"/>')
    A(f'<path d="{d}L1147 349H780Z" fill="url(#growth-fill)"/>')
    A(f'<path d="{d}" fill="none" stroke="#a78bfa" stroke-width="2.5" stroke-linecap="round"/>')
    A(f'<circle r="3" fill="{INK}"><animateMotion path="{d}" dur="6s" repeatCount="indefinite"/></circle>')
    for xx,yy,label in milestones:
        A(f'<path d="M{xx} {yy+8}V356" stroke="#818cf8" stroke-opacity=".2" stroke-dasharray="2 5"/>')
        A(f'<circle cx="{xx}" cy="{yy}" r="3.5" fill="{BG}" stroke="{VIO}" stroke-width="1.5"/>')
        anchor='end' if label=='Production' else 'start' if label=='Python' else 'middle'
        A(P(label,'mono',9.5,xx,380,fill=MID,anchor=anchor))
    A(f'<circle cx="1147" cy="138" r="8" fill="{LIME}" opacity=".15"><animate attributeName="r" values="5;12;5" dur="2.5s" repeatCount="indefinite"/></circle><circle cx="1147" cy="138" r="4" fill="{LIME}"/>')
    A(P('BUILDING ON WHAT I KNOW','mono-b',9.5,1148,122,fill=LIME,anchor='end'))
    A(P('Learning -> building -> shipping','mono',10,770,402,fill=VIO))
    A(P('Illustrative','mono',9,1150,402,fill=DIM,anchor='end'))
    save(o,'model-card.svg')

if __name__=='__main__':
    for args in [('01','Model card','about.md',"who is behind the weights"),('02','Forward pass','stack/','the tools, connected'),('03','Inference graph','production/','NexAI Labs in production'),('04','Detections','projects/',"things I have shipped"),('05','Live signal','activity/','generated from GitHub')]:heading(*args)
    model_card();print('Built five section bars and the model card.')
