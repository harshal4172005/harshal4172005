"""Shared outlined typography and SVG primitives for Harshal's profile."""
from pathlib import Path
from html import escape
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT=Path(__file__).resolve().parents[1]
BG='#09090b'; LINE='#27272a'; INK='#f4f4f5'; MID='#a1a1aa'; DIM='#71717a'
IND='#818cf8'; VIO='#b18af5'; LIME='#b6ed47'; RED='#f43f5e'; AMB='#facc15'; CYAN='#4fc4e4'
fonts={key:TTFont('C:/Windows/Fonts/'+name) for key,name in [('mono','consola.ttf'),('mono-m','consola.ttf'),('mono-b','consolab.ttf'),('serif','BOD_CR.TTF'),('serif-i','BOD_CI.TTF')]}

def width(s,font,size,ls=0):
    f=fonts[font];g=f.getGlyphSet();cm=f.getBestCmap();scale=size/f['head'].unitsPerEm
    return sum(g[cm.get(ord(c),'.notdef')].width*scale for c in s)+max(0,len(s)-1)*ls

def path(s,font,size,x,y,ls=0):
    f=fonts[font];g=f.getGlyphSet();cm=f.getBestCmap();scale=size/f['head'].unitsPerEm
    pen=SVGPathPen(g);start=x
    for c in s:
        name=cm.get(ord(c),'.notdef');g[name].draw(TransformPen(pen,(scale,0,0,-scale,x,y)))
        x+=g[name].width*scale+ls
    return pen.getCommands(),x-start-ls if s else 0

def P(s,font,size,x,y,fill=INK,ls=0,anchor='start',extra=''):
    w=width(s,font,size,ls)
    if anchor=='end':x-=w
    elif anchor=='middle':x-=w/2
    d,_=path(s,font,size,x,y,ls)
    return f'<path d="{d}" fill="{fill}" aria-label="{escape(s,quote=True)}" {extra}/>'

def open_svg(w,h,title,aur=(.5,.5,.5),corners=True):
    defs='''<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".65" fill="#27272a"/></pattern><linearGradient id="iv"><stop stop-color="#818cf8"/><stop offset="1" stop-color="#c084fc"/></linearGradient><radialGradient id="aur"><stop stop-color="#818cf8" stop-opacity=".06"/><stop offset="1" stop-color="#09090b" stop-opacity="0"/></radialGradient><filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2"/></filter></defs>'''
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">',f'<title>{escape(title)}</title>',defs,f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/><rect width="{w}" height="{h}" rx="14" fill="url(#dots)" opacity=".65"/><rect width="{w}" height="{h}" rx="14" fill="url(#aur)"/><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{LINE}"/>']
    if corners:
        o.append(f'<path d="M16 34V16H34M{w-34} 16H{w-16}V34M16 {h-34}V{h-16}H34M{w-34} {h-16}H{w-16}V{h-34}" fill="none" stroke="#71717a"/>')
    return o

def save(o,name):
    (ROOT/'assets'/name).write_text('\n'.join(o+['</svg>']),encoding='utf-8')

def segs(items,x,y,font='mono',size=12):
    out=''
    for s,color in items:
        out+=P(s,font,size,x,y,fill=color);x+=width(s,font,size)
    return out,x
