import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('stats',Path(__file__).resolve().parents[1]/'scripts/generate_stats.py')
stats=importlib.util.module_from_spec(spec);spec.loader.exec_module(stats)

class ActivityTests(unittest.TestCase):
    def fixture(self):
        commit={'oid':'abc1234','messageHeadline':'fix: <parser> & "quotes"','committedDate':'2026-11-06T00:00:00Z','url':'https://github.com/test/commit/abc1234','author':{'user':{'login':stats.USER}}}
        repo={'name':'actual-work','url':'https://github.com/test','isFork':False,'stargazerCount':2,'pushedAt':'2026-11-06T00:00:00Z','languages':{'edges':[{'size':80,'node':{'name':'Python','color':'#3572a5'}},{'size':20,'node':{'name':'C#','color':'#777777'}}]},'defaultBranchRef':{'target':{'history':{'nodes':[commit]}}}}
        return {'repositories':{'pageInfo':{'hasNextPage':False},'nodes':[repo]},'contributionsCollection':{'contributionCalendar':{'totalContributions':3,'weeks':[{'contributionDays':[{'date':'2026-11-06','contributionCount':3}]}]},'totalPullRequestContributions':0,'totalIssueContributions':0}}

    def test_real_counts_and_unfiltered_language_bytes(self):
        d=stats.normalize(self.fixture())
        self.assertEqual(d['contributions'],3)
        self.assertEqual(d['stars'],2)
        self.assertEqual(d['languages'][1]['name'],'C#')
        self.assertEqual(sum(x['bytes'] for x in d['languages']),100)

    def test_forks_unattributed_commits_and_empty_branches(self):
        u=self.fixture();r=copy.deepcopy(u['repositories']['nodes'][0]);r['isFork']=True;r['defaultBranchRef']=None
        u['repositories']['nodes'].append(r)
        u['repositories']['nodes'][0]['defaultBranchRef']['target']['history']['nodes'][0]['author']['user']=None
        d=stats.normalize(u)
        self.assertEqual(d['public_repos'],2)
        self.assertEqual(d['stars'],2)
        self.assertEqual(d['recent_commits'],[])

    def test_pagination_cannot_silently_truncate_totals(self):
        u=self.fixture();u['repositories']['pageInfo']['hasNextPage']=True
        with self.assertRaises(RuntimeError): stats.normalize(u)

    def test_xml_escapes_commit_content_and_handles_zero_activity(self):
        d=stats.normalize(self.fixture());ET.fromstring(stats.render(d))
        d.update(weeks=[],recent_commits=[],languages=[])
        ET.fromstring(stats.render(d))

    def test_publish_is_idempotent_and_updates_cache_key(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'assets').mkdir()
            (root/'README.md').write_text('assets/activity-field.svg?v=initial\n<!-- ACTIVITY:START -->\n<!-- ACTIVITY:END -->',encoding='utf-8')
            with patch.object(stats,'ROOT',root):
                d=stats.normalize(self.fixture());stats.publish(d)
                before={p:p.read_bytes() for p in root.rglob('*') if p.is_file()}
                stats.publish(d)
                self.assertEqual(before,{p:p.read_bytes() for p in root.rglob('*') if p.is_file()})
                self.assertNotIn('?v=initial',(root/'README.md').read_text())
                self.assertIn('/commit/',(root/'README.md').read_text())

if __name__=='__main__': unittest.main()
