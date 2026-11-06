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
    o=open_svg(1200,460,'Harshal Parekh model card: AI engineering background and an illustrative journey from notebooks to production.')
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
    A(P('ILLUSTRATIVE LOSS · notebook -> production','mono',9.5,770,101,fill=DIM,ls=.2))
    train=[];val=[]
    for i in range(65):
        xx=770+i*5.93
        base=122+222*(1-math.exp(-i/13))
        train.append((xx,base+random.uniform(-5,5)))
        val.append((xx,base-7+random.uniform(-10,7)))
    for pts,color in [(train,IND),(val,VIO)]:
        d='M'+' L'.join(f'{xx:.1f} {yy:.1f}' for xx,yy in pts)
        A(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.6" stroke-dasharray="1500" stroke-dashoffset="0"><animate attributeName="stroke-dashoffset" values="1500;0;0" keyTimes="0;.7;1" dur="9s" repeatCount="indefinite"/></path>')
    xx,yy=train[-1]
    A(f'<circle cx="{xx}" cy="{yy}" r="7" fill="{LIME}" opacity=".18"><animate attributeName="r" values="4;10;4" dur="2s" repeatCount="indefinite"/></circle><circle cx="{xx}" cy="{yy}" r="3.5" fill="{LIME}"/>')
    A(f'<path d="M{xx} {yy-5}V286" stroke="{LIME}" stroke-dasharray="2 3" opacity=".6"/>')
    A(P('shipped / deployed','mono-b',10,1151,282,fill=LIME,anchor='end'))
    for xx,label in [(770,'jupyter'),(846,'fastapi'),(945,'docker'),(1047,'ec2'),(1125,'prod')]:A(P(label,'mono',9.5,xx,380,fill=DIM))
    A(P('Illustration of the engineering journey','mono',9,1150,400,fill='#52525b',anchor='end'))
    save(o,'model-card.svg')

if __name__=='__main__':
    for args in [('01','Model card','about.md',"who is behind the weights"),('02','Forward pass','stack/','the tools, connected'),('03','Inference graph','production/','NexAI Labs in production'),('04','Detections','projects/',"things I have shipped"),('05','Live signal','activity/','generated from GitHub')]:heading(*args)
    model_card();print('Built five section bars and the model card.')
