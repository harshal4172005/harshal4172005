"""Build four independently clickable contact cards for GitHub image embedding."""
from common import *

items=[('email','Email','START A CONVERSATION',LIME),('linkedin','LinkedIn','CONNECT WITH ME',VIO),('resume','Resume','EXPERIENCE / SKILLS',IND),('source','Source code','INSPECT THE BUILDS',CYAN)]
for i,(key,title,subtitle,color) in enumerate(items):
    o=open_svg(280,84,title+' — '+subtitle,corners=False)
    A=o.append
    A(f'<style>@keyframes trace{{to{{stroke-dashoffset:-580}}}}.trace{{animation:trace 12s linear infinite;animation-delay:-{i*2}s}}@media(prefers-reduced-motion:reduce){{.trace{{animation:none}}}}</style>')
    A(f'<path d="M15 83H265" stroke="{color}" opacity=".18"/>')
    A(f'<path d="M15 83H265" stroke="{color}" stroke-width="1.3" stroke-dasharray="28 552" stroke-dashoffset="0" class="trace"/>')
    A(f'<rect x="16" y="22" width="36" height="36" rx="10" fill="{color}" fill-opacity=".08" stroke="{color}" stroke-opacity=".25"/>')
    if key=='email':
        A(f'<g fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="25" y="33" width="18" height="14" rx="2"/><path d="M25 34l9 7 9-7"/></g>')
    elif key=='linkedin':A(P('in','mono-b',22,34,47,fill=color,anchor='middle'))
    elif key=='resume':
        A(f'<g fill="none" stroke="{color}" stroke-width="1.4" stroke-linejoin="round"><path d="M28 30h9l5 5v16H28zM37 30v6h5M31 40h7M31 44h7M31 48h5"/></g>')
    else:A(f'<path d="M29 34l-6 6 6 6M39 34l6 6-6 6M36 31l-4 18" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    A(P(title,'serif',27,65,40,fill=INK))
    A(P(subtitle,'mono',8,66,58,fill=DIM,ls=.6))
    A(f'<path d="M247 28h10v10M257 28l-12 12" fill="none" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>')
    save(o,'contact-'+key+'.svg')
print('Built four contact buttons.')
