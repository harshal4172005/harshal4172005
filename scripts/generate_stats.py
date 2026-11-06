"""Verified activity renderer. Standard library only; failures preserve the last snapshot."""
import collections
import datetime as dt
import hashlib
import html
import json
import math
import os
import re
from pathlib import Path
import subprocess
import time
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
USER = 'harshal4172005'
QUERY = '''query { user(login:"harshal4172005") {
  contributionsCollection { totalCommitContributions contributionCalendar { totalContributions weeks {
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

def streaks(weeks, today=None):
    """Compute calendar streaks, allowing the current day to remain open."""
    today = today or dt.datetime.now(dt.timezone.utc).date()
    counts = {dt.date.fromisoformat(day['date']): day['contributionCount']
              for week in weeks for day in week['contributionDays']
              if dt.date.fromisoformat(day['date']) <= today}
    end = today if counts.get(today, 0) else today - dt.timedelta(days=1)
    current = 0
    while counts.get(end, 0) > 0:
        current += 1
        end -= dt.timedelta(days=1)
    longest = run = 0
    if counts:
        cursor = min(counts)
        while cursor <= today:
            run = run + 1 if counts.get(cursor, 0) > 0 else 0
            longest = max(longest, run)
            cursor += dt.timedelta(days=1)
    return {'today': counts.get(today, 0), 'current': current,
            'longest': longest, 'active_days': sum(n > 0 for n in counts.values()),
            'as_of': today.isoformat(), 'calendar_timezone': 'UTC'}

def normalize(user):
    if user['repositories']['pageInfo']['hasNextPage']:
        raise RuntimeError('More than 100 repositories: add pagination before publishing totals')
    repos = user['repositories']['nodes']
    original = [r for r in repos if not r['isFork']]
    langs=collections.Counter(); colors={}; commits=[]
    for r in original:
        for e in r['languages']['edges']:
            name=e['node']['name']
            langs[name]+=e['size']; colors[name]=e['node']['color'] or '#a78bfa'
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
    return {'streaks':streaks(coll['contributionCalendar']['weeks']),
            'commits':coll['totalCommitContributions'],
            'contributions':coll['contributionCalendar']['totalContributions'],
            'weeks':coll['contributionCalendar']['weeks'],
            'prs':coll['totalPullRequestContributions'],
            'issues':coll['totalIssueContributions'],
            'public_repos':len(repos),'stars':sum(r['stargazerCount'] for r in original),
            'languages':[{'name':n,'bytes':v,'color':colors[n]} for n,v in langs.most_common()],
            'recent_commits':list(unique.values())[:4]}

def t(s,x,y,size=14,color='#f4f4f5'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{html.escape(str(s))}</text>'

def render(data):
    c=t('GITHUB ACTIVITY / VERIFIED',32,39,18,'#b6ed47')
    c+=t('CHECKED EVERY 30 MIN / '+data['streaks']['as_of'],790,39,11,'#8b8b95')
    c+='<path d="M32 62H1168" stroke="#27272a"/>'
    for x,num,label in [(32,data['contributions'],'API CONTRIBUTIONS / PAST YEAR'),(450,data['public_repos'],'PUBLIC REPOSITORIES'),(870,data['stars'],'STARS / OWNED NON-FORKS')]:
        c+=t(f'{num:,}',x,127,47)+t(label,x,153,12,'#8b8b95')
    c+='<path d="M32 178H1168" stroke="#27272a"/>'
    streak=data['streaks']
    for x,key,label in [(32,'today','CONTRIBUTIONS TODAY'),(325,'current','CURRENT STREAK / DAYS'),(618,'longest','LONGEST STREAK / PAST YEAR'),(911,'active_days','ACTIVE DAYS / PAST YEAR')]:
        c+=t(streak[key],x,229,35,'#b6ed47' if key=='current' else '#a78bfa')
        c+=t(label,x,254,11,'#8b8b95')
    c+=t('COMMIT TOPOGRAPHY',32,298,12,'#b6ed47')
    c+=t('Each ridge is a week. Height follows contribution count.',32,321,12,'#8b8b95')
    weeks=data['weeks'][-53:]
    maximum=max([d['contributionCount'] for w in weeks for d in w['contributionDays']]+[1])
    for i,w in enumerate(weeks):
        base_x=43+i*17.6; base_y=457-i*.91; pts=[]
        for j in range(7):
            days=w['contributionDays']
            count=days[j]['contributionCount'] if j<len(days) else 0
            height=math.log1p(count)/math.log1p(maximum)*78
            pts.append((base_x+j*20,base_y+j*9-height))
        path='M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
        c+=f'<path d="{path}" fill="none" stroke="{"#b6ed47" if i==len(weeks)-1 else "#a78bfa"}" stroke-width="{2 if i==len(weeks)-1 else 1}" opacity="{.3+.7*i/len(weeks):.2f}"/>'
    if weeks: c+=f'<circle r="3" fill="#b6ed47"><animateMotion dur="7s" repeatCount="indefinite" path="{path}"/></circle>'
    c+=t('OLDER',33,543,11,'#8b8b95')+t('LATEST ->',1010,543,11,'#b6ed47')
    c+='<path d="M32 566H1168" stroke="#27272a"/>'
    c+=t('LATEST AUTHORED COMMITS / PUBLIC DEFAULT BRANCHES',32,597,12,'#b6ed47')
    for i,commit in enumerate(data['recent_commits']):
        y=633+i*53; title=commit['messageHeadline']
        if len(title)>78: title=title[:75]+'...'
        c+=t(commit['oid'][:7],32,y,13,'#a78bfa')+t(title,145,y,14)
        c+=t(commit['repo'][:68],145,y+19,11,'#8b8b95')
        c+=t(commit['committedDate'][:10],1050,y,12,'#8b8b95')
    if not data['recent_commits']: c+=t('No matching authored commits in the sampled default-branch histories.',32,637)
    c+='<path d="M32 851H1168" stroke="#27272a"/>'
    c+=t('LANGUAGE BYTES / PUBLIC OWNED NON-FORK REPOSITORIES',32,883,12,'#b6ed47')
    total=sum(l['bytes'] for l in data['languages']); x=32
    for lang in data['languages']:
        width=1136*lang['bytes']/total if total else 0
        c+=f'<rect x="{x}" y="902" width="{width}" height="8" fill="{lang["color"]}"/>'
        x+=width
    for i,lang in enumerate(data['languages'][:5]):
        c+=t(f'{lang["name"]} {lang["bytes"]/total:.1%}',32+i*226,940,12)
    c+=t('Streaks use GitHub calendar dates (UTC). Yesterday keeps a streak active while today is still open.',32,979,11,'#8b8b95')
    c+=t('Counts reflect API access and can differ from signed-in totals. No private repository details are published.',32,998,11,'#8b8b95')
    c+=t('Commits: latest 12 per default branch. Languages: code size; top 20 per public owned non-fork repository.',32,1017,10,'#8b8b95')
    return '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1040" viewBox="0 0 1200 1040" role="img"><title>Live GitHub activity and daily contribution streaks for Harshal Parekh</title><style>text{font-family:Consolas,monospace}</style><rect width="1200" height="1040" rx="14" fill="#09090b"/><rect x=".5" y=".5" width="1199" height="1039" rx="14" fill="none" stroke="#27272a"/>'+c+'</svg>'

def render_header(header, commits):
    updated, matches = re.subn(r'(<text id="live-commit-count"[^>]*>)[^<]*(</text>)',
                               lambda m: m[1] + f'{commits:,}' + m[2], header)
    if matches != 1:
        raise ValueError('Expected one live commit counter in the hero SVG')
    ET.fromstring(updated)
    return updated

def publish(data):
    snapshot=ROOT/'data/activity.json'
    canonical=json.dumps(data,sort_keys=True,ensure_ascii=False,indent=2)+'\n'
    old=json.loads(snapshot.read_text(encoding='utf-8')) if snapshot.exists() else None
    svg=render(data); ET.fromstring(svg)
    header_path=ROOT/'assets/hero-header.svg'
    old_header=header_path.read_text(encoding='utf-8')
    header=render_header(old_header,data['commits'])
    readme=ROOT/'README.md'; content=readme.read_text(encoding='utf-8')
    digest=hashlib.sha256(canonical.encode()).hexdigest()[:12]
    import re
    content=re.sub(r'assets/activity-field\.svg\?v=[a-zA-Z0-9]+',f'assets/activity-field.svg?v={digest}',content)
    header_digest=hashlib.sha256(header.encode()).hexdigest()[:12]
    content=re.sub(r'assets/hero-header\.svg\?v=[a-zA-Z0-9]+',f'assets/hero-header.svg?v={header_digest}',content)
    start='<!-- ACTIVITY:START -->'; end='<!-- ACTIVITY:END -->'
    links='\n'.join(f'- [{c["oid"][:7]}]({c["url"]}) · `{c["repo"]}` · {c["committedDate"][:10]}' for c in data['recent_commits'])
    if start in content and end in content:
        a,b=content.split(start,1); _,z=b.split(end,1)
        content=a+start+'\n'+links+'\n'+end+z
    if old_header==header and old==data and (ROOT/'assets/activity-field.svg').read_text(encoding='utf-8')==svg and readme.read_text(encoding='utf-8')==content:
        print('No activity change; no commit needed.'); return
    snapshot.parent.mkdir(exist_ok=True)
    header_path.write_text(header,encoding='utf-8')
    snapshot.write_text(canonical,encoding='utf-8')
    (ROOT/'assets/activity-field.svg').write_text(svg,encoding='utf-8')
    readme.write_text(content,encoding='utf-8')
    print('Published verified activity, contribution landscape and language bytes.')

if __name__=='__main__': publish(normalize(fetch()))
