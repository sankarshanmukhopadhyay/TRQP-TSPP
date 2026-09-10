#!/usr/bin/env python3
"""Independent TSPP-side evidence-state and material-lifecycle validator.

This module intentionally does not import the downstream TRQP reference evaluator.
It models TSPP invalidation observations for assurance evidence only.
"""
from datetime import datetime, timezone


def ts(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)


def evaluate(source, principals, query):
    at = ts(query['time'])
    observed = ts(source['observed_at'])
    if not source['authoritative']:
        return ('unknown', 'source-non-authoritative')
    if at > observed and (at - observed).total_seconds() > source['fresh_for_seconds']:
        return ('stale', 'source-stale')
    unsupported = set(query.get('critical_context', [])) - set(source.get('supported_context', []))
    if unsupported:
        return ('unknown', 'critical-condition-unsupported')
    if query.get('historical') and not source['history_complete']:
        return ('unknown', 'history-incomplete')

    principal = next((p for p in principals if p['id'] == query['entity_id']), None)
    if principal is None:
        return ('negative', 'absent-complete') if source['complete_for_scope'] else ('unknown', 'absence-incomplete')

    material_id = query.get('verification_material')
    if material_id is None:
        return ('positive', 'principal-current')
    material = next((m for m in principal['materials'] if m['id'] == material_id), None)
    if material is None:
        return ('negative', 'material-absent-complete') if source['complete_for_scope'] else ('unknown', 'material-absence-incomplete')

    if material.get('valid_from') and at < ts(material['valid_from']):
        return ('negative', 'material-not-yet-applicable')
    if material.get('valid_until') and at >= ts(material['valid_until']):
        return ('negative', 'material-expired-or-superseded')
    if material.get('revoked_at') and at >= ts(material['revoked_at']):
        return ('negative', 'material-revoked')
    if material['purpose'] != query['action']:
        return ('negative', 'purpose-not-applicable')
    if material['resource'] != query['resource']:
        return ('negative', 'resource-not-applicable')
    return ('positive', 'material-current')


def legacy_drop_critical_material(source, principals, query):
    degraded = dict(query)
    degraded.pop('verification_material', None)
    degraded['critical_context'] = []
    return evaluate(source, principals, degraded)
