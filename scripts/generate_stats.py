"""Verified activity renderer. Standard library only; failures preserve the last snapshot."""
import collections
import hashlib
import html
import json
import math
import os
from pathlib import Path
import subprocess
import time
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
USER = 'harshal4172005'
QUERY = '''query { user(login:"harshal4172005") {
  contributionsCollection { contributionCalendar { totalContributions weeks {
    contributionDays { date contributionCount }
  } } totalPullRequestContributions totalIssueContributions }
  repositories(first:100,privacy:PUBLIC,ownerAffiliations:OWNER,
    orderBy:{field:PUSHED_AT,direction:DESC}) {
    pageInfo { hasNextPage }
    nodes { name url isFork stargazerCount pushedAt
      languages(first:20,orderBy:{field:SIZE,direction:DESC}) {
        edges { size node { name color } }
      }
      defaultBranchRef { target { ... on Commit { history(first:12) {
        nodes { oid messageHeadline committedDate url author { user { login } } }
      } } } }
    }
  }
} }'''

def fetch():
    token = os.environ.get('GITHUB_TOKEN')
    for attempt in range(3):
        try:
            if token:
                req = urllib.request.Request('https://api.github.com/graphql',
                    data=json.dumps({'query':QUERY}).encode(),
                    headers={'Authorization':f'Bearer {token}',
                             'Content-Type':'application/json', 'User-Agent':'harshal-profile'})
                with urllib.request.urlopen(req, timeout=60) as response:
                    result = json.load(response)
            else:
                result = json.loads(subprocess.run(
                    ['gh','api','graphql','-f','query='+QUERY],check=True,
                    capture_output=True,text=True,encoding='utf-8').stdout)
            if result.get('errors'):
                raise RuntimeError('GitHub GraphQL returned errors; preserving previous snapshot')
            return result['data']['user']
        except Exception:
            if attempt == 2: raise
            time.sleep(2 ** attempt)

def normalize(user):
    if user['repositories']['pageInfo']['hasNextPage']:
        raise RuntimeError('More than 100 repositories: add pagination before publishing totals')
    repos = user['repositories']['nodes']
    original = [r for r in repos if not r['isFork']]
    langs=collections.Counter(); colors={}; commits=[]
    for r in original:
        for e in r['languages']['edges']:
            name=e['node']['name']
            langs[name]+=e['size']; colors[name]=e['node']['color'] or '#a9baff'
    for r in repos:
        branch=r.get('defaultBranchRef')
        if not branch: continue
        for c in branch['target']['history']['nodes']:
            author=c.get('author') or {}
            if (author.get('user') or {}).get('login','').lower()!=USER: continue
            if r['name']==USER and c['messageHeadline'].startswith('chore(activity):'): continue
            commits.append({**{k:c[k] for k in ['oid','messageHeadline','committedDate','url']},'repo':r['name']})
    commits=sorted(commits,key=lambda c:c['committedDate'],reverse=True)
    unique={}
    for c in commits: unique.setdefault(c['oid'],c)
    coll=user['contributionsCollection']
    return {'contributions':coll['contributionCalendar']['totalContributions'],
            'weeks':coll['contributionCalendar']['weeks'],
            'prs':coll['totalPullRequestContributions'],
            'issues':coll['totalIssueContributions'],
            'public_repos':len(repos),'stars':sum(r['stargazerCount'] for r in original),
            'languages':[{'name':n,'bytes':v,'color':colors[n]} for n,v in langs.most_common()],
            'recent_commits':list(unique.values())[:4]}

def t(s,x,y,size=14,color='#eeeae0'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{html.escape(str(s))}</text>'

def render(data):
    c=t('04 / THE LIVING REPOSITORY',32,39,18,'#d4fc67')
    c+=t('GITHUB DATA / CHECKED EVERY 30 MIN',777,39,12,'#92999e')
    c+='<path d="M32 62H1168" stroke="#343b42"/>'
    for x,num,label in [(32,data['contributions'],'CONTRIBUTIONS / PAST YEAR'),(450,data['public_repos'],'PUBLIC REPOSITORIES'),(870,data['stars'],'STARS / OWNED NON-FORKS')]:
        c+=t(f'{num:,}',x,127,47)+t(label,x,153,12,'#92999e')
    c+=t('COMMIT TOPOGRAPHY',32,201,12,'#d4fc67')
    c+=t('Each ridge is a week. Height follows contribution count.',32,224,12,'#92999e')
    weeks=data['weeks'][-53:]
    maximum=max([d['contributionCount'] for w in weeks for d in w['contributionDays']]+[1])
    for i,w in enumerate(weeks):
        base_x=43+i*17.6; base_y=360-i*.91; pts=[]
        for j in range(7):
            days=w['contributionDays']
            count=days[j]['contributionCount'] if j<len(days) else 0
            height=math.log1p(count)/math.log1p(maximum)*78
            pts.append((base_x+j*20,base_y+j*9-height))
        path='M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
        c+=f'<path d="{path}" fill="none" stroke="{"#d4fc67" if i==len(weeks)-1 else "#a9baff"}" stroke-width="{2 if i==len(weeks)-1 else 1}" opacity="{.3+.7*i/len(weeks):.2f}"/>'
    if weeks: c+=f'<circle r="3" fill="#d4fc67"><animateMotion dur="7s" repeatCount="indefinite" path="{path}"/></circle>'
    c+=t('OLDER',33,446,11,'#92999e')+t('LATEST ->',1010,446,11,'#d4fc67')
    c+='<path d="M32 469H1168" stroke="#343b42"/>'
    c+=t('LATEST AUTHORED COMMITS / PUBLIC DEFAULT BRANCHES',32,500,12,'#d4fc67')
    for i,commit in enumerate(data['recent_commits']):
        y=536+i*53; title=commit['messageHeadline']
        if len(title)>78: title=title[:75]+'...'
        c+=t(commit['oid'][:7],32,y,13,'#a9baff')+t(title,145,y,14)
        c+=t(commit['repo'][:68],145,y+19,11,'#92999e')
        c+=t(commit['committedDate'][:10],1050,y,12,'#92999e')
    if not data['recent_commits']: c+=t('No matching authored commits in the sampled default-branch histories.',32,540)
    c+='<path d="M32 754H1168" stroke="#343b42"/>'
    c+=t('LANGUAGE BYTES / PUBLIC OWNED NON-FORK REPOSITORIES',32,786,12,'#d4fc67')
    total=sum(l['bytes'] for l in data['languages']); x=32
    for lang in data['languages']:
        width=1136*lang['bytes']/total if total else 0
        c+=f'<rect x="{x}" y="805" width="{width}" height="8" fill="{lang["color"]}"/>'
        x+=width
    for i,lang in enumerate(data['languages'][:5]):
        c+=t(f'{lang["name"]} {lang["bytes"]/total:.1%}',32+i*226,843,12)
    c+=t('Contribution totals may include private aggregates; no private repository details are published.',32,885,11,'#92999e')
    c+=t('Commits: latest 12 per default branch. Languages: code size, not proficiency. Top 20 languages per repository.',32,904,10,'#92999e')
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="930" viewBox="0 0 1200 930" role="img"><title>Live engineering activity for Harshal Parekh</title><style>text{font-family:Consolas,'Liberation Mono',monospace}</style><rect width="1200" height="930" fill="#101319"/>'''+c+'</svg>'

def publish(data):
    snapshot=ROOT/'data/activity.json'
    canonical=json.dumps(data,sort_keys=True,ensure_ascii=False,indent=2)+'\n'
    old=json.loads(snapshot.read_text(encoding='utf-8')) if snapshot.exists() else None
    svg=render(data); ET.fromstring(svg)
    readme=ROOT/'README.md'; content=readme.read_text(encoding='utf-8')
    digest=hashlib.sha256(canonical.encode()).hexdigest()[:12]
    import re
    content=re.sub(r'assets/activity-field\.svg\?v=[a-zA-Z0-9]+',f'assets/activity-field.svg?v={digest}',content)
    start='<!-- ACTIVITY:START -->'; end='<!-- ACTIVITY:END -->'
    links='\n'.join(f'- [{c["oid"][:7]}]({c["url"]}) · `{c["repo"]}` · {c["committedDate"][:10]}' for c in data['recent_commits'])
    if start in content and end in content:
        a,b=content.split(start,1); _,z=b.split(end,1)
        content=a+start+'\n'+links+'\n'+end+z
    if old==data and (ROOT/'assets/activity-field.svg').read_text(encoding='utf-8')==svg and readme.read_text(encoding='utf-8')==content:
        print('No activity change; no commit needed.'); return
    snapshot.parent.mkdir(exist_ok=True)
    snapshot.write_text(canonical,encoding='utf-8')
    (ROOT/'assets/activity-field.svg').write_text(svg,encoding='utf-8')
    readme.write_text(content,encoding='utf-8')
    print('Published verified activity, contribution landscape and language bytes.')

if __name__=='__main__': publish(normalize(fetch()))
