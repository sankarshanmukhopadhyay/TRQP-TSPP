import unittest

from build_profile_consumable_posture import build


BASE_REPORT = {
    "run_id": "run-1",
    "target_id": "registry-1",
    "generated_at": "2026-09-10T00:00:00Z",
    "assurance_level": "AL2",
    "summary": {"PASS": 1, "FAIL": 0, "NOT_TESTED": 0},
    "results": [{"control_id": "TSPP-AL2-01", "status": "PASS", "evidence": "fixture"}],
}


def make(**kwargs):
    params = dict(
        report=BASE_REPORT,
        tspp_version="0.16.1",
        control_set_id="tspp-control-registry",
        control_set_revision="abc123",
        reassessment_state="CURRENT",
    )
    params.update(kwargs)
    return build(**params)


class ProfileConsumablePostureTests(unittest.TestCase):
    def test_preserves_target_run_control_set_and_level(self):
        evidence = make()
        self.assertEqual(evidence["target"]["id"], "registry-1")
        self.assertEqual(evidence["run"]["id"], "run-1")
        self.assertEqual(evidence["control_set"]["revision"], "abc123")
        self.assertEqual(evidence["assurance_level"], "AL2")

    def test_profile_metadata_cannot_override_posture(self):
        a = make()
        b = make(profile_context={"id": "ayra-trqp", "version": "0.6.0-draft"})
        self.assertEqual(a["posture"], b["posture"])

    def test_posture_relevant_profile_change_requires_reassessment(self):
        evidence = make(profile_context={"id": "ayra-trqp", "source_changed": True, "posture_relevant": True})
        self.assertEqual(evidence["reassessment"]["state"], "REASSESS_REQUIRED")

    def test_unknown_profile_change_impact_fails_safe(self):
        evidence = make(profile_context={"id": "ayra-trqp", "source_changed": True})
        self.assertEqual(evidence["reassessment"]["state"], "REASSESS_REQUIRED")

    def test_posture_irrelevant_profile_change_can_remain_current_with_rationale(self):
        evidence = make(profile_context={"id": "ayra-trqp", "source_changed": True, "posture_relevant": False})
        self.assertEqual(evidence["reassessment"]["state"], "CURRENT")
        self.assertEqual(evidence["reassessment"]["rationale_code"], "profile-change-posture-non-material")

    def test_missing_control_evidence_never_becomes_pass(self):
        report = dict(BASE_REPORT)
        report["summary"] = {"PASS": 0, "FAIL": 0, "NOT_TESTED": 1}
        report["results"] = [{"control_id": "TSPP-SIGN-01", "status": "NOT_TESTED"}]
        evidence = make(report=report)
        self.assertEqual(evidence["posture"]["result"], "INDETERMINATE")
        self.assertEqual(evidence["posture"]["controls"][0]["result"], "INDETERMINATE")

    def test_same_posture_can_be_correlated_to_multiple_profiles(self):
        a = make(profile_context={"id": "ayra-trqp"})
        b = make(profile_context={"id": "other-profile"})
        self.assertEqual(a["posture"], b["posture"])

    def test_existing_invalid_state_cannot_be_weakened_by_profile_metadata(self):
        evidence = make(reassessment_state="INVALID", profile_context={"id": "ayra-trqp", "source_changed": True, "posture_relevant": False})
        self.assertEqual(evidence["reassessment"]["state"], "INVALID")


if __name__ == "__main__":
    unittest.main()
