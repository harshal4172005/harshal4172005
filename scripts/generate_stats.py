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
  contributionsCollection { restrictedContributionsCount totalCommitContributions contributionCalendar { totalContributions weeks {
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
            'private_contributions':coll['restrictedContributionsCount'],
            'public_contributions':coll['contributionCalendar']['totalContributions']-coll['restrictedContributionsCount'],
            'weeks':coll['contributionCalendar']['weeks'],
            'prs':coll['totalPullRequestContributions'],
            'issues':coll['totalIssueContributions'],
            'public_repos':len(repos),'stars':sum(r['stargazerCount'] for r in original),
            'languages':[{'name':n,'bytes':v,'color':colors[n]} for n,v in langs.most_common()],
            'recent_commits':list(unique.values())[:4]}

def t(s,x,y,size=14,color='#f4f4f5'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{html.escape(str(s))}</text>'

def render(data):
    c=t('GITHUB ACTIVITY',28,45,24,'#b6ed47')+t('SYNC / EVERY 10 MIN',615,44,15,'#a0a2b0')
    c+='<path d="M28 66H812" stroke="#27272a"/>'
    c+=t(f'{data["contributions"]:,}',28,140,64)+t('TOTAL CONTRIBUTIONS / PAST YEAR',28,173,17,'#c3c5ce')
    c+=t(f'{data["public_contributions"]:,} public + {data["private_contributions"]:,} private',28,204,18,'#a78bfa')
    for x,key,label in [(510,'public_repos','Public repos'),(690,'stars','Stars')]:
        c+=t(data[key],x,140,46)+t(label,x,173,17,'#c3c5ce')
    c+='<path d="M28 228H812" stroke="#27272a"/>'
    for x,key,label,sub in [(28,'today','TODAY','contributions'),(235,'current','CURRENT STREAK','days'),(442,'longest','LONGEST STREAK','past year'),(649,'active_days','ACTIVE DAYS','past year')]:
        c+=t(data['streaks'][key],x,289,44,'#b6ed47' if key=='current' else '#a78bfa')
        c+=t(label,x,320,15,'#c3c5ce')+t(sub,x,344,15,'#a0a2b0')
    c+=t('CONTRIBUTION LANDSCAPE',28,393,20,'#b6ed47')
    c+=t('One ridge per week. Height follows daily contributions.',28,423,16,'#c3c5ce')
    weeks=data['weeks'][-53:]
    maximum=max([d['contributionCount'] for w in weeks for d in w['contributionDays']]+[1])
    for i,w in enumerate(weeks):
        pts=[]
        for j in range(7):
            days=w['contributionDays'];count=days[j]['contributionCount'] if j<len(days) else 0
            height=math.log1p(count)/math.log1p(maximum)*72
            pts.append((32+i*12.7+j*14,535-i*.55+j*7-height))
        path='M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
        c+=f'<path d="{path}" fill="none" stroke="{"#b6ed47" if i==len(weeks)-1 else "#a78bfa"}" stroke-width="{2 if i==len(weeks)-1 else 1}" opacity="{.3+.7*i/len(weeks):.2f}"/>'
    if weeks:c+=f'<circle r="3" fill="#b6ed47"><animateMotion dur="7s" repeatCount="indefinite" path="{path}"/></circle>'
    c+=t('OLDER',28,614,14,'#a0a2b0')+t('LATEST',745,614,14,'#b6ed47')
    c+='<path d="M28 637H812" stroke="#27272a"/>'
    c+=t('LATEST AUTHORED COMMITS',28,678,20,'#b6ed47')
    for i,commit in enumerate(data['recent_commits']):
        y=718+i*64;title=commit['messageHeadline']
        if len(title)>65:title=title[:62]+'...'
        c+=t(commit['oid'][:7],28,y,15,'#a78bfa')+t(title,123,y,16.5)
        c+=t(commit['repo'][:48],123,y+26,15,'#c3c5ce')+t(commit['committedDate'][:10],680,y+26,14,'#a0a2b0')
    if not data['recent_commits']:c+=t('No matching public authored commits yet.',28,718,17)
    c+='<path d="M28 970H812" stroke="#27272a"/>'
    c+=t('LANGUAGES / PUBLIC CODE BYTES',28,1010,20,'#b6ed47')
    total=sum(l['bytes'] for l in data['languages']);x=28
    for lang in data['languages']:
        w=784*lang['bytes']/total if total else 0
        c+=f'<rect x="{x}" y="1032" width="{w}" height="11" fill="{lang["color"]}"/>';x+=w
    for i,lang in enumerate(data['languages'][:6]):
        c+=t(f'{lang["name"]} {lang["bytes"]/total:.1%}',28+(i%3)*267,1075+(i//3)*28,16,'#c3c5ce')
    return '<svg xmlns="http://www.w3.org/2000/svg" width="840" height="1130" viewBox="0 0 840 1130" role="img"><title>Live public and private contribution totals, daily streaks, commits and language bytes</title><style>text{font-family:Consolas,monospace}</style><rect width="840" height="1130" rx="14" fill="#09090b"/><rect x=".5" y=".5" width="839" height="1129" rx="14" fill="none" stroke="#27272a"/>'+c+'</svg>'

def render_header(header, contributions):
    updated, matches = re.subn(r'(<text id="live-contribution-count"[^>]*>)[^<]*(</text>)',
                               lambda m: m[1] + f'{contributions:,}' + m[2], header)
    if matches != 1:
        raise ValueError('Expected one live contribution counter in the hero SVG')
    ET.fromstring(updated)
    return updated

def publish(data):
    snapshot=ROOT/'data/activity.json'
    canonical=json.dumps(data,sort_keys=True,ensure_ascii=False,indent=2)+'\n'
    old=json.loads(snapshot.read_text(encoding='utf-8')) if snapshot.exists() else None
    svg=render(data); ET.fromstring(svg)
    header_path=ROOT/'assets/hero-total-readable.svg'
    old_header=header_path.read_text(encoding='utf-8')
    header=render_header(old_header,data['contributions'])
    readme=ROOT/'README.md'; content=readme.read_text(encoding='utf-8')
    digest=hashlib.sha256(canonical.encode()).hexdigest()[:12]
    import re
    content=re.sub(r'assets/activity-readable\.svg\?v=[a-zA-Z0-9]+',f'assets/activity-readable.svg?v={digest}',content)
    header_digest=hashlib.sha256(header.encode()).hexdigest()[:12]
    content=re.sub(r'assets/hero-total-readable\.svg\?v=[a-zA-Z0-9]+',f'assets/hero-total-readable.svg?v={header_digest}',content)
    start='<!-- ACTIVITY:START -->'; end='<!-- ACTIVITY:END -->'
    links='\n'.join(f'- [{c["oid"][:7]}]({c["url"]}) · `{c["repo"]}` · {c["committedDate"][:10]}' for c in data['recent_commits'])
    if start in content and end in content:
        a,b=content.split(start,1); _,z=b.split(end,1)
        content=a+start+'\n'+links+'\n'+end+z
    metrics_start='<!-- METRICS:START -->';metrics_end='<!-- METRICS:END -->'
    if metrics_start in content and metrics_end in content:
        a,b=content.split(metrics_start,1);_,z=b.split(metrics_end,1)
        summary=(f'**Total contributions: {data["contributions"]:,}** — '
                 f'{data["public_contributions"]:,} public + {data["private_contributions"]:,} private.\n\n'
                 f'**Today:** {data["streaks"]["today"]:,} contributions · '
                 f'**Current streak:** {data["streaks"]["current"]} days · '
                 f'**Longest streak:** {data["streaks"]["longest"]} days in the past year.')
        content=a+metrics_start+'\n'+summary+'\n'+metrics_end+z
    if old_header==header and old==data and (ROOT/'assets/activity-readable.svg').read_text(encoding='utf-8')==svg and readme.read_text(encoding='utf-8')==content:
        print('No activity change; no commit needed.'); return
    snapshot.parent.mkdir(exist_ok=True)
    header_path.write_text(header,encoding='utf-8')
    snapshot.write_text(canonical,encoding='utf-8')
    (ROOT/'assets/activity-readable.svg').write_text(svg,encoding='utf-8')
    readme.write_text(content,encoding='utf-8')
    print('Published verified activity, contribution landscape and language bytes.')

if __name__=='__main__': publish(normalize(fetch()))
