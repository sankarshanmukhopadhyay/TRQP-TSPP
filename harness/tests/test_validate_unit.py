from tspp_trqp_harness.validate import assert_freshness, iso8601_like, require_fields, validate_json


def test_iso8601_like_accepts_rfc3339_zulu():
    assert iso8601_like("2026-03-06T12:30:00Z") is True


def test_iso8601_like_rejects_non_datetime_text():
    assert iso8601_like("2026/03/06 12:30:00") is False


def test_require_fields_accepts_present_fields():
    require_fields({"a": 1, "b": 2}, ("a", "b"))


def test_require_fields_rejects_missing_fields():
    try:
        require_fields({"a": 1}, ("a", "b"))
    except AssertionError as exc:
        assert "Missing required fields" in str(exc)
    else:
        raise AssertionError("require_fields should fail when fields are missing")


def test_assert_freshness_accepts_valid_meta():
    assert_freshness({"time_evaluated": "2026-03-06T12:00:00Z", "expires_at": "2026-03-06T12:05:00Z"})


def test_assert_freshness_rejects_invalid_meta():
    try:
        assert_freshness({"time_evaluated": "bad", "expires_at": "2026-03-06T12:05:00Z"})
    except AssertionError as exc:
        assert "time_evaluated" in str(exc)
    else:
        raise AssertionError("assert_freshness should fail for invalid time_evaluated")


def test_validate_json_accepts_matching_schema():
    schema = {
        "type": "object",
        "required": ["status"],
        "properties": {"status": {"type": "string"}},
        "additionalProperties": False,
    }
    validate_json({"status": "ok"}, schema)


def test_validate_json_rejects_nonmatching_schema():
    schema = {
        "type": "object",
        "required": ["status"],
        "properties": {"status": {"type": "string"}},
        "additionalProperties": False,
    }
    try:
        validate_json({"status": 1}, schema)
    except Exception:
        return
    raise AssertionError("validate_json should fail for invalid instance")
