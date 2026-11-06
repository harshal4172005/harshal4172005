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
        return {'repositories':{'pageInfo':{'hasNextPage':False},'nodes':[repo]},'contributionsCollection':{'restrictedContributionsCount':1,'totalCommitContributions':2,'contributionCalendar':{'totalContributions':3,'weeks':[{'contributionDays':[{'date':'2026-11-06','contributionCount':3}]}]},'totalPullRequestContributions':0,'totalIssueContributions':0}}

    def test_real_counts_and_unfiltered_language_bytes(self):
        d=stats.normalize(self.fixture())
        self.assertEqual(d['contributions'],3)
        self.assertEqual(d['commits'],2)
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
            (root/'assets/hero-total-readable.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"><text id="live-contribution-count">0</text></svg>')
            (root/'README.md').write_text('assets/activity-readable.svg?v=initial\n<!-- METRICS:START --><!-- METRICS:END -->\n<!-- ACTIVITY:START -->\n<!-- ACTIVITY:END -->',encoding='utf-8')
            with patch.object(stats,'ROOT',root):
                d=stats.normalize(self.fixture());stats.publish(d)
                before={p:p.read_bytes() for p in root.rglob('*') if p.is_file()}
                stats.publish(d)
                self.assertEqual(before,{p:p.read_bytes() for p in root.rglob('*') if p.is_file()})
                self.assertNotIn('?v=initial',(root/'README.md').read_text())
                self.assertIn('/commit/',(root/'README.md').read_text())
                self.assertIn('>3</text>',(root/'assets/hero-total-readable.svg').read_text())
                self.assertIn('**Total contributions: 3**',(root/'README.md').read_text())
                d['contributions']=4; d['public_contributions']=3
                stats.publish(d)
                self.assertIn('**Total contributions: 4**',(root/'README.md').read_text())
                self.assertIn('>4</text>',(root/'assets/hero-total-readable.svg').read_text())


    def test_header_uses_exact_contribution_count_and_formats_thousands(self):
        h='<svg xmlns="http://www.w3.org/2000/svg"><text id="live-contribution-count">100</text></svg>'
        out=stats.render_header(h,1234)
        self.assertIn('>1,234</text>',out)
        self.assertIn('>0</text>',stats.render_header(h,0))
        with self.assertRaises(ValueError): stats.render_header('<svg/>',3)

    def test_total_already_includes_private_contributions(self):
        user=self.fixture()
        user['contributionsCollection']['contributionCalendar']['totalContributions']=1060
        user['contributionsCollection']['restrictedContributionsCount']=529
        data=stats.normalize(user)
        self.assertEqual(data['contributions'],1060)
        self.assertEqual(data['public_contributions'],531)
        self.assertEqual(data['private_contributions'],529)
        self.assertIn('>1,060</text>',stats.render(data))
        self.assertNotIn('>1,589</text>',stats.render(data))

    def test_current_streak_counts_today_and_yesterday(self):
        weeks=[{'contributionDays':[{'date':'2026-11-04','contributionCount':1},{'date':'2026-11-05','contributionCount':4},{'date':'2026-11-06','contributionCount':2}]}]
        d=stats.streaks(weeks,stats.dt.date(2026,11,6))
        self.assertEqual(d['current'],3)
        self.assertEqual(d['today'],2)
        self.assertEqual(d['longest'],3)
        self.assertEqual(d['active_days'],3)

    def test_open_today_keeps_yesterdays_streak(self):
        weeks=[{'contributionDays':[{'date':'2026-11-04','contributionCount':1},{'date':'2026-11-05','contributionCount':4},{'date':'2026-11-06','contributionCount':0}]}]
        self.assertEqual(stats.streaks(weeks,stats.dt.date(2026,11,6))['current'],2)

    def test_missed_day_resets_current_but_preserves_longest(self):
        weeks=[{'contributionDays':[{'date':'2026-11-03','contributionCount':1},{'date':'2026-11-04','contributionCount':4},{'date':'2026-11-05','contributionCount':0},{'date':'2026-11-06','contributionCount':0}]}]
        d=stats.streaks(weeks,stats.dt.date(2026,11,6))
        self.assertEqual(d['current'],0)
        self.assertEqual(d['longest'],2)

    def test_missing_calendar_days_break_streak(self):
        weeks=[{'contributionDays':[{'date':'2026-11-04','contributionCount':1},{'date':'2026-11-06','contributionCount':2}]}]
        self.assertEqual(stats.streaks(weeks,stats.dt.date(2026,11,6))['current'],1)

    def test_future_dates_are_excluded(self):
        weeks=[{'contributionDays':[{'date':'2026-11-07','contributionCount':10}]}]
        d=stats.streaks(weeks,stats.dt.date(2026,11,6))
        self.assertEqual(d['current'],0)
        self.assertEqual(d['active_days'],0)

    def test_empty_calendar_is_zero(self):
        d=stats.streaks([],stats.dt.date(2026,11,6))
        self.assertEqual((d['current'],d['longest'],d['today']),(0,0,0))

if __name__=='__main__': unittest.main()
