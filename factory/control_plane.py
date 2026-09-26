"""Deterministic control plane for Kiln factory runs."""
from __future__ import annotations
import argparse, json, uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / 'factory' / 'runs'
STAGES = ['architect','modeler','builder','adversary','repairer','verifier']

def path(run_id): return RUNS / f'{run_id}.json'

def load(run_id):
    p = path(run_id)
    if not p.exists(): raise SystemExit(f'run not found: {run_id}')
    return json.loads(p.read_text(encoding='utf-8'))

def save(run):
    RUNS.mkdir(parents=True, exist_ok=True)
    path(run['run_id']).write_text(json.dumps(run, indent=2)+'\n', encoding='utf-8')

def init_run(requirement):
    run={'run_id':uuid.uuid4().hex[:12],'requirement':requirement,'stages':[{'name':s,'status':'pending','artifact':None} for s in STAGES]}
    save(run); return run

def advance(run, stage, artifact):
    i=STAGES.index(stage); current=run['stages'][i]
    if current['status'] != 'pending': raise SystemExit(f'stage {stage} is already {current["status"]}')
    if i and (run['stages'][i-1]['status'] != 'passed' or not run['stages'][i-1]['artifact']):
        raise SystemExit(f'cannot start {stage}: previous stage must be passed with an artifact')
    current['status']='passed'; current['artifact']=artifact; save(run)

def show(run):
    print(f"run_id={run['run_id']}")
    print(f"requirement={run['requirement']}")
    for s in run['stages']: print(f"{s['name']}: {s['status']} [{s['artifact'] or '-'}]")

def main():
    p=argparse.ArgumentParser(description='Kiln factory control plane'); sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('init'); a.add_argument('requirement')
    a=sub.add_parser('status'); a.add_argument('run_id')
    a=sub.add_parser('advance'); a.add_argument('run_id'); a.add_argument('stage',choices=STAGES); a.add_argument('artifact')
    args=p.parse_args()
    if args.command=='init': print(init_run(args.requirement)['run_id']); return 0
    run=load(args.run_id)
    if args.command=='status': show(run); return 0
    advance(run,args.stage,args.artifact); show(load(args.run_id)); return 0

if __name__=='__main__': raise SystemExit(main())