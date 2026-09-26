"""Validate Kiln factory artifacts before they enter the evidence chain."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(relative: str) -> dict:
    with (ROOT / relative).open(encoding='utf-8') as handle:
        return json.load(handle)

def check_keys(name: str, document: dict, keys: tuple[str, ...]) -> list[str]:
    return [f'{name}: missing {key}' for key in keys if key not in document]

def main() -> int:
    errors: list[str] = []
    handoff = load('factory/artifacts/example-handoff.json')
    errors.extend(check_keys('handoff', handoff, ('stage','task','inputs','outputs','changed_files','tests','evidence','open_failures','next_action')))
    verification = load('factory/artifacts/example-verification.json')
    errors.extend(check_keys('verification', verification, ('run_id','requirement','stages')))
    run = load('factory/artifacts/run-template.json')
    errors.extend(check_keys('run template', run, ('run_id','requirement','stages')))
    for label, document in (('verification', verification), ('run template', run)):
        if not isinstance(document.get('stages'), list) or not document['stages']:
            errors.append(f'{label}: stages must be a non-empty list')
    if errors:
        print('ARTIFACT VALIDATION FAILED')
        for error in errors: print(f'- {error}')
        return 1
    print('ARTIFACT VALIDATION PASSED')
    print('handoff=valid')
    print('verification=valid')
    print('run_template=valid')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())