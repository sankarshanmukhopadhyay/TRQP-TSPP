#!/usr/bin/env python3
import unittest
from wp8_evidence_validator import evaluate, legacy_drop_critical_material


def source(**overrides):
    value = dict(authoritative=True, complete_for_scope=True, history_complete=True,
                 observed_at='2026-09-10T00:00:00Z', fresh_for_seconds=7*24*60*60,
                 supported_context=['verification_material', 'time'])
    value.update(overrides)
    return value


PRINCIPALS = [{'id': 'did:example:issuer-a', 'materials': [
    {'id': 'C1', 'purpose': 'issue', 'resource': 'credential-x', 'valid_from': '2026-01-01T00:00:00Z', 'valid_until': '2026-07-01T00:00:00Z'},
    {'id': 'C2', 'purpose': 'issue', 'resource': 'credential-x', 'valid_from': '2026-07-01T00:00:00Z', 'revoked_at': '2026-09-01T00:00:00Z'},
    {'id': 'C3', 'purpose': 'verify', 'resource': 'credential-x', 'valid_from': '2026-07-01T00:00:00Z'},
    {'id': 'C4', 'purpose': 'issue', 'resource': 'credential-y', 'valid_from': '2026-07-01T00:00:00Z'}]}]


def query(**overrides):
    value = dict(entity_id='did:example:issuer-a', action='issue', resource='credential-x',
                 verification_material='C2', time='2026-08-15T00:00:00Z',
                 critical_context=['verification_material'])
    value.update(overrides)
    return value


class WP8EvidenceTests(unittest.TestCase):
    def expect(self, expected, q=None, s=None):
        self.assertEqual(expected, evaluate(s or source(), PRINCIPALS, q or query()))

    def test_current_material_positive(self): self.expect(('positive', 'material-current'))
    def test_revoked_material_negative(self): self.expect(('negative', 'material-revoked'), query(time='2026-09-05T00:00:00Z'))
    def test_complete_absence_negative(self): self.expect(('negative', 'absent-complete'), query(entity_id='did:example:absent'))
    def test_incomplete_absence_unknown(self): self.expect(('unknown', 'absence-incomplete'), query(entity_id='did:example:absent'), source(complete_for_scope=False))
    def test_non_authoritative_unknown(self): self.expect(('unknown', 'source-non-authoritative'), s=source(authoritative=False))
    def test_stale_evidence(self): self.expect(('stale', 'source-stale'), query(time='2026-09-20T00:00:00Z'))
    def test_historical_prior_material(self): self.expect(('positive', 'material-current'), query(verification_material='C1', time='2026-06-01T00:00:00Z', historical=True))
    def test_incomplete_history_unknown(self): self.expect(('unknown', 'history-incomplete'), query(verification_material='C1', time='2026-06-01T00:00:00Z', historical=True), source(history_complete=False))
    def test_wrong_purpose(self): self.expect(('negative', 'purpose-not-applicable'), query(verification_material='C3'))
    def test_wrong_resource(self): self.expect(('negative', 'resource-not-applicable'), query(verification_material='C4'))
    def test_unknown_material_complete(self): self.expect(('negative', 'material-absent-complete'), query(verification_material='UNKNOWN'))
    def test_unknown_material_incomplete(self): self.expect(('unknown', 'material-absence-incomplete'), query(verification_material='UNKNOWN'), source(complete_for_scope=False))
    def test_unsupported_critical_condition(self): self.expect(('unknown', 'critical-condition-unsupported'), s=source(supported_context=['time']))
    def test_expired_or_superseded(self): self.expect(('negative', 'material-expired-or-superseded'), query(verification_material='C1', time='2026-08-15T00:00:00Z'))
    def test_before_validity(self): self.expect(('negative', 'material-not-yet-applicable'), query(time='2026-06-01T00:00:00Z', historical=True))

    def test_legacy_drop_is_detectably_unsafe(self):
        q = query(verification_material='UNKNOWN')
        self.assertEqual(('negative', 'material-absent-complete'), evaluate(source(), PRINCIPALS, q))
        self.assertEqual(('positive', 'principal-current'), legacy_drop_critical_material(source(), PRINCIPALS, q))


if __name__ == '__main__':
    unittest.main()
