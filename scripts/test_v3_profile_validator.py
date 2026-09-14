#!/usr/bin/env python3
import unittest

from v3_profile_validator import (
    CANDIDATE_SHA,
    PRINCIPALS,
    evaluate_profile_boundary,
    query,
    semantic_class,
    source,
    validate,
)
from wp8_evidence_validator import evaluate as evaluate_wp8


class CandidateV3ProfileTests(unittest.TestCase):
    def test_complete_requirement_mapping_and_pin(self):
        report = validate()
        self.assertEqual(CANDIDATE_SHA, report["candidate_commit"])
        self.assertEqual(32, report["mapped_requirements"])

    def test_stale_and_unknown_map_to_indeterminate(self):
        stale = evaluate_wp8(source(), PRINCIPALS, query(time="2026-09-20T00:00:00Z"))
        unknown = evaluate_wp8(
            source(supported_context=["time"]), PRINCIPALS, query()
        )
        self.assertEqual("indeterminate", semantic_class(stale))
        self.assertEqual("indeterminate", semantic_class(unknown))

    def test_historical_state_is_evaluated_as_of_time(self):
        observation = evaluate_wp8(
            source(),
            PRINCIPALS,
            query(verification_material="C1", time="2026-06-01T00:00:00Z", historical=True),
        )
        self.assertEqual("positive", semantic_class(observation))

    def test_no_silent_v3_to_v2_fallback(self):
        self.assertEqual(
            {"semantic_decision": "indeterminate", "processing": "reject"},
            evaluate_profile_boundary({"requested_version": "v2", "legacy_fallback": True}),
        )

    def test_transport_failure_is_not_semantic_negative(self):
        self.assertEqual(
            {"semantic_decision": "indeterminate", "processing": "reject"},
            evaluate_profile_boundary({"transport_ok": False}),
        )

    def test_recognition_is_non_transitive_by_default(self):
        self.assertEqual(
            {"semantic_decision": "negative", "processing": "accept"},
            evaluate_profile_boundary({"recognition_transitive_without_authority": True}),
        )


if __name__ == "__main__":
    unittest.main()
