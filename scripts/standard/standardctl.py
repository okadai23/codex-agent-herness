#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class CheckResult:
    level: str
    message: str


def run_cmd(cmd: list[str], cwd: Path) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)
        out = (p.stdout + "\n" + p.stderr).strip()
        return p.returncode, out
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"


def load_standard_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    data: dict[str, object] = {}
    section = None
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith('#'):
            continue
        if ':' in line and not line.startswith(' '):
            k, v = line.split(':', 1)
            key = k.strip()
            val = v.strip().strip('"\'')
            if not val:
                data[key] = {}
                section = key
            else:
                data[key] = val
                section = None
        elif section and ':' in line and line.startswith(' '):
            k, v = line.strip().split(':', 1)
            sec = data.get(section)
            if isinstance(sec, dict):
                sec[k.strip()] = v.strip().strip('"\'')
    return data


def expected_paths_for_profile(profile: str) -> list[str]:
    mapping = {
        'ts-fullstack': ['apps/web', 'apps/api', 'packages/api-contract'],
        'python-ai-service': ['pyproject.toml', 'tests', 'prompts'],
        'hybrid-product': ['apps/web', 'apps/api', 'pyproject.toml', 'services/ai'],
    }
    return mapping.get(profile, [])


def doctor(root: Path) -> int:
    checks: list[CheckResult] = []
    required = ['standard.yml', 'apm.yml', 'apm.lock.yaml']
    optional_warn = ['.copier-answers.yml']

    for name in required:
        checks.append(CheckResult('OK' if (root / name).exists() else 'ERROR', f'{name}'))
    for name in optional_warn:
        checks.append(CheckResult('OK' if (root / name).exists() else 'WARN', f'{name}'))

    std = load_standard_yaml(root / 'standard.yml')
    template = std.get('template')
    profile = ''
    if isinstance(template, dict):
        profile = str(template.get('profile', '')).strip()
    if not profile:
        profile = str(std.get('profile', '')).strip()
    for p in expected_paths_for_profile(profile):
        level = 'OK' if (root / p).exists() else 'ERROR'
        checks.append(CheckResult(level, f'profile-required: {p}'))

    errors = [c for c in checks if c.level == 'ERROR']
    for c in checks:
        print(f'[{c.level}] {c.message}')
    return 1 if errors else 0


def drift(root: Path) -> int:
    cmds = [
        ['copier', 'check-update'],
        ['apm', 'outdated'],
        ['pnpm', 'api:generate', '--check'],
        ['pnpm', 'docs:verify'],
        ['apm', 'compile', '--validate'],
    ]
    results = []
    for cmd in cmds:
        code, out = run_cmd(cmd, root)
        results.append({'cmd': ' '.join(cmd), 'code': code, 'output': out[:2000]})
    print('## standardctl drift report')
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 1 if any(r['code'] != 0 for r in results) else 0


def update_template(root: Path) -> int:
    code, out = run_cmd(['copier', 'check-update'], root)
    if code != 0:
        print(out)
        return code
    if 'No updates' in out or 'up to date' in out.lower():
        print('No template update found.')
        return 0
    ucode, uout = run_cmd(['copier', 'update', '--defaults', '--conflict', 'rej'], root)
    print(uout)
    rej = list(root.rglob('*.rej'))
    if rej:
        print('Conflict files detected:', ', '.join(str(p) for p in rej))
        return 1
    return ucode


def update_harness(root: Path) -> int:
    cmds = [
        ['apm', 'outdated'],
        ['apm', 'update'],
        ['apm', 'audit', '--ci', '--policy', 'org'],
        ['apm', 'compile', '--validate'],
    ]
    for cmd in cmds:
        code, out = run_cmd(cmd, root)
        joined = ' '.join(cmd)
        print(f'$ {joined}\n{out}\n')
        if code != 0:
            return code
    return 0


def apply_section(root: Path, section: str) -> int:
    code = 0
    if section in {'api-contract-openapi', 'ts-fullstack'}:
        code, _ = run_cmd([
            'copier',
            'update',
            '--defaults',
            '--conflict',
            'rej',
            '--data',
            f'sections.{section}=true',
        ], root)
        if code != 0:
            return code
    code, _ = run_cmd(['apm', 'install'], root)
    if code != 0:
        return code
    verify_cmd = ['apm', 'compile', '--validate']
    verify_code, verify_out = run_cmd(verify_cmd, root)

    diff_code, diff_out = run_cmd(['git', 'status', '--short'], root)
    if diff_code != 0:
        diff_out = 'git status unavailable'

    unresolved_risks = []
    if verify_code != 0:
        unresolved_risks.append('apm compile --validate failed')
    if '.rej' in diff_out:
        unresolved_risks.append('copier reject files detected')

    report_dir = root / 'docs' / 'harness' / 'adoptions'
    report_dir.mkdir(parents=True, exist_ok=True)
    date = dt.datetime.now(dt.UTC).strftime('%Y-%m-%d')
    report = report_dir / f'{date}-{section}.md'
    risk_lines = '\n'.join(f'- {r}' for r in unresolved_risks) if unresolved_risks else '- なし'
    report.write_text(
        f"# Adoption report: {section}\n\n"
        f"- date: {date}\n"
        f"- section: {section}\n"
        f"\n## 変更内容\n\n"
        f"```\n{diff_out}\n```\n"
        f"\n## 検証コマンド\n\n"
        f"- {' '.join(verify_cmd)} (exit_code={verify_code})\n"
        f"\n## 検証出力\n\n```\n{verify_out}\n```\n"
        f"\n## 未解決リスク\n\n{risk_lines}\n",
        encoding='utf-8',
    )
    print(f'Wrote report: {report}')
    return verify_code


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='standardctl')
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('doctor')
    sub.add_parser('drift')
    aps = sub.add_parser('apply')
    aps.add_argument('--section', required=True)
    sub.add_parser('update-template')
    sub.add_parser('update-harness')
    return p


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path.cwd()
    if args.cmd == 'doctor':
        return doctor(root)
    if args.cmd == 'drift':
        return drift(root)
    if args.cmd == 'apply':
        return apply_section(root, args.section)
    if args.cmd == 'update-template':
        return update_template(root)
    if args.cmd == 'update-harness':
        return update_harness(root)
    return 2


if __name__ == '__main__':
    sys.exit(main())
