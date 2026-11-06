"""Forward-pass stack and packet-routed production architecture."""
import random
from common import *
random.seed(21)
W=1200

def forward_pass():
    o=open_svg(W,470,'Technology stack as a neural network forward pass; connections illustrate a toolchain, not measured model weights.')
    A=o.append
    cols=[(96,175,'L0 · LANGUAGES',AMB,['Python','C#','JavaScript','SQL']),
          (380,115,'L1 · ML / VISION',VIO,['PyTorch','TensorFlow','YOLOv8','OpenCV','Diffusion','LangChain','Gemini']),
          (664,95,'L2 · SERVING & DATA',IND,['FastAPI','Flask','.NET 8','React','SignalR','Redis','PostgreSQL','Qdrant']),
          (948,135,'L3 · INFRA & CLOUD',CYAN,['Docker','AWS','GCP','Cloudflare R2','n8n','Linux'])]
    PW,PH=168,30
    curves=[]
    for idx in range(3):
        x,y,_,_,items=cols[idx];nx,ny,_,_,nextitems=cols[idx+1]
        for i in range(len(items)):
            for j in range(len(nextitems)):
                sy=y+i*40+15;ey=ny+j*40+15
                d=f'M{x+PW} {sy}C{x+PW+52} {sy} {nx-52} {ey} {nx} {ey}'
                A(f'<path d="{d}" fill="none" stroke="#34313e" stroke-width=".65" opacity=".45"/>')
                curves.append((d,cols[idx][3]))
    for x,y,heading,color,items in cols:
        A(P(heading,'mono',11,x,61,fill=color,ls=1.5))
        A(f'<path d="M{x} 74h{PW}" stroke="{color}" opacity=".25"/>')
        for i,item in enumerate(items):
            yy=y+i*40
            A(f'<rect x="{x}" y="{yy}" width="{PW}" height="{PH}" rx="7" fill="#0e0e13" stroke="{color}" stroke-opacity=".4"/>')
            A(f'<circle cx="{x+14}" cy="{yy+15}" r="3" fill="{color}"/>')
            A(P(item,'mono-m',13,x+26,yy+20,fill=INK))
    # Draw signals on top of the nodes' connecting lines; labels contain no fake weights.
    for k in range(22):
        d,color=curves[(k*17)%len(curves)];begin=round(k*.3,2)
        A(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-dasharray="40 1000" stroke-dashoffset="70"><animate attributeName="stroke-dashoffset" values="70;-1000" begin="{begin}s" dur="3.4s" repeatCount="indefinite"/></path>')
    A(segs([('x = ',DIM),('idea',AMB)],96,436)[0])
    A(P('y = model(x)  # -> something running in production','mono',12,1104,436,fill=MID,anchor='end'))
    save(o,'forward-pass.svg')

def inference_graph():
    o=open_svg(W,440,'NexAI Labs production architecture: n8n, FastAPI, diffusion and video generation, AWS S3 and Cloudflare R2 serving commercial brands.')
    A=o.append
    A(P('NEXAI LABS','mono-b',11,44,50,fill=IND,ls=1.8))
    A(P('env=production  ·  runtime=docker  ·  host=aws-ec2','mono',11,150,50,fill=DIM,ls=.4))
    label='ALL SYSTEMS LIVE'
    A(f'<circle cx="{W-56-width(label,"mono-m",10.5,1.2)}" cy="46" r="3.5" fill="{LIME}"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>')
    A(P(label,'mono-m',10.5,W-44,50,fill=LIME,ls=1.2,anchor='end'))
    A(f'<rect x="254" y="88" width="440" height="264" rx="10" fill="#818cf8" fill-opacity=".035" stroke="#818cf8" stroke-opacity=".25" stroke-dasharray="4 5"/>')
    A(P('docker · ec2','mono',10,266,80,fill=IND,ls=1))
    nodes={'client':(44,194,'CLIENT','prompt / media',AMB),'router':(272,118,'n8n ROUTER','multi-agent',VIO),
           'api':(272,268,'FASTAPI','microservice',IND),'diffusion':(500,118,'DIFFUSION','image pipeline',VIO),
           'video':(500,268,'VIDEO GEN','generation pipeline',IND),'s3':(728,118,'AWS S3','asset store',CYAN),
           'r2':(728,268,'CLOUDFLARE R2','delivery',CYAN),'brands':(980,194,'5+ BRANDS','garment · jewelry',LIME)}
    def port(n,side):
        x,y,*_=nodes[n];return (x+176 if side=='r' else x,y+33)
    def curve(a,b):
        x,y=a;xx,yy=b;return f'M{x} {y}C{x+40} {y} {xx-40} {yy} {xx} {yy}'
    edges=[('client','router'),('router','diffusion'),('diffusion','s3'),('api','video'),('video','r2'),('s3','brands'),('r2','brands')]
    routes={f'{a}-{b}':curve(port(a,'r'),port(b,'l')) for a,b in edges}
    routes['router-api']='M360 184V268';routes['diffusion-video']='M588 184V268'
    for d in routes.values():A(f'<path d="{d}" fill="none" stroke="#3f3f46" stroke-width="1.3"/>')
    # Boxes precede the moving packets, so packets remain visible through transitions.
    for key,(x,y,title,sub,color) in nodes.items():
        A(f'<rect x="{x}" y="{y}" width="176" height="66" rx="10" fill="#0d0d12" stroke="{LINE}"/>')
        A(f'<path d="M{x+10} {y}h32" stroke="{color}" stroke-width="1.5"/>')
        A(P(title,'mono-b',13,x+16,y+29,fill=INK,ls=.7))
        A(P(sub,'mono',11.5,x+16,y+49,fill=DIM))
        A(f'<circle cx="{x+160}" cy="{y+24}" r="3" fill="{color}" opacity=".55"/>')
    packet_routes=[('client-router','i2v_job',LIME,0),('router-diffusion','img_job',VIO,1),('diffusion-s3','img_job',VIO,2),('router-api','vid_job',IND,.6),('api-video','vid_job',IND,1.6),('video-r2','vid_job',CYAN,2.6),('s3-brands','asset',LIME,3),('r2-brands','asset',CYAN,3.6)]
    for key,label,color,begin in packet_routes:
        d=routes[key];tw=width(label,'mono-b',9)+10
        A(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="30 1000" opacity=".8"><animate attributeName="stroke-dashoffset" values="50;-350" begin="{begin}s" dur="5s" repeatCount="indefinite"/></path>')
        A(f'<g opacity="0"><animateMotion path="{d}" dur="5s" begin="{begin}s" repeatCount="indefinite" keyPoints="0;0;1;1" keyTimes="0;.04;.55;1" calcMode="linear"/><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.04;.5;.56;1" dur="5s" begin="{begin}s" repeatCount="indefinite"/><rect x="{-tw/2}" y="-23" width="{tw}" height="16" rx="3" fill="{color}"/>'+P(label,'mono-b',9,0,-12,fill=BG,anchor='middle')+'</g>')
    for x,value,label in [(44,'5+','commercial brands in prod'),(296,'60%','faster creative turnaround'),(574,'2','pipelines · image + video'),(812,'1','n8n brain routing it all')]:
        A(P(value,'mono-m',26,x,398,fill=VIO));A(P(label,'mono',11,x+width(value,'mono-m',26)+10,394,fill=MID))
    save(o,'inference-graph.svg')

if __name__=='__main__':forward_pass();inference_graph();print('Built forward pass and live inference graph.')
