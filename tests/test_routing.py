import unittest
from routing import assign

class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.team, self.loads = ['A', 'B'], {'A': 5, 'B': 1}
    def test_continuity_before_load(self):
        self.assertEqual(assign({}, self.team, self.loads, recent_owner='A')['owner'], 'A')
    def test_deduplicate_open_request(self):
        self.assertEqual(assign({}, self.team, self.loads, open_owner='A')['action'], 'merge')
    def test_declined_owner_excluded(self):
        self.assertEqual(assign({}, self.team, self.loads, recent_owner='A', declined=['A'])['owner'], 'B')
    def test_no_owner_is_review_not_silent_loss(self):
        self.assertEqual(assign({}, self.team, self.loads, declined=self.team)['action'], 'manual_review')
    def test_contact_opt_out_overrides_everything(self):
        self.assertEqual(assign({'do_not_contact': True}, self.team, self.loads, open_owner='A')['action'], 'suppress')
    def test_explicit_owner_overrides_history(self):
        self.assertEqual(assign({'explicit_owner': 'B'}, self.team, self.loads, recent_owner='A')['owner'], 'B')
    def test_unknown_owner_uses_workload(self):
        self.assertEqual(assign({}, self.team, self.loads, recent_owner='UNKNOWN')['owner'], 'B')
    def test_deterministic_tie(self):
        self.assertEqual(assign({}, ['B', 'A'], {})['owner'], 'A')
