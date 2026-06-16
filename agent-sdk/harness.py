import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    print('Missing dependency: pyyaml')
    sys.exit(1)

ALLOWED_SURFACE = {
    'FOUND',
    'NOT_FOUND',
    'VERSION_DRIFT',
    'CRAWLER_BLOCKED'
}

FORBIDDEN_FIELDS = {
    'risk_score',
    'trust_score',
    'corruption_score',
    'sentiment',
    'dangerous',
    'liable',
    'motive',
    'intent'
}

ALLOWED_AGENT_KINDS = {
    'observer',
    'verifier',
    'detector',
    'tombstone'
}

ALLOWED_LIFECYCLE = {
    'active',
    'deprecated',
    'retired'
}


def fail(msg):
    print(f'FAIL: {msg}')
    sys.exit(1)


def load_manifest(path_str):
    path = pathlib.Path(path_str)

    if not path.exists():
        fail(f'manifest not found: {path}')

    with path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        fail('manifest must be object')

    return data


def validate_closed_world(manifest):
    allowed_keys = {
        'agent_id',
        'kind',
        'lifecycle',
        'constitutional_basis',
        'allowed_domains',
        'allowed_url_schemes',
        'allowed_verdicts',
        'forbidden_fields',
        'runtime',
        'targets_file'
    }

    extra = set(manifest.keys()) - allowed_keys

    if extra:
        fail(f'unconstitutional manifest fields: {sorted(extra)}')


def validate_agent_kind(manifest):
    kind = manifest.get('kind')

    if kind not in ALLOWED_AGENT_KINDS:
        fail(f'forbidden agent kind: {kind}')


def validate_lifecycle(manifest):
    lifecycle = manifest.get('lifecycle')

    if lifecycle not in ALLOWED_LIFECYCLE:
        fail(f'invalid lifecycle: {lifecycle}')


def validate_verdicts(manifest):
    verdicts = manifest.get('allowed_verdicts', [])

    if not isinstance(verdicts, list):
        fail('allowed_verdicts must be list')

    unknown = set(verdicts) - ALLOWED_SURFACE

    if unknown:
        fail(f'unknown verdicts: {sorted(unknown)}')


def validate_forbidden_fields(manifest):
    fields = manifest.get('forbidden_fields', [])

    if not isinstance(fields, list):
        fail('forbidden_fields must be list')

    missing = FORBIDDEN_FIELDS - set(fields)

    if missing:
        fail(f'missing forbidden fields: {sorted(missing)}')


def validate_domains(manifest):
    domains = manifest.get('allowed_domains', [])

    if not isinstance(domains, list):
        fail('allowed_domains must be list')

    for d in domains:
        if not isinstance(d, str):
            fail(f'invalid domain entry: {d}')


def validate_url_schemes(manifest):
    schemes = manifest.get('allowed_url_schemes', [])

    if schemes != ['https']:
        fail('only https allowed')


def validate_runtime(manifest):
    runtime = manifest.get('runtime')

    if not isinstance(runtime, dict):
        fail('runtime missing')

    if 'max_requests_per_run' not in runtime:
        fail('runtime.max_requests_per_run missing')


def main():
    if len(sys.argv) != 2:
        print('usage: python agent-sdk/harness.py <manifest.yaml>')
        sys.exit(1)

    manifest = load_manifest(sys.argv[1])

    validate_closed_world(manifest)
    validate_agent_kind(manifest)
    validate_lifecycle(manifest)
    validate_verdicts(manifest)
    validate_forbidden_fields(manifest)
    validate_domains(manifest)
    validate_url_schemes(manifest)
    validate_runtime(manifest)

    print(json.dumps({
        'status': 'PASS',
        'agent_id': manifest.get('agent_id'),
        'kind': manifest.get('kind'),
        'lifecycle': manifest.get('lifecycle'),
        'no_ghost_anchor': True
    }, indent=2))


if __name__ == '__main__':
    main()
