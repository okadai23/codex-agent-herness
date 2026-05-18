from __future__ import annotations

import tempfile
from pathlib import Path

from scripts.standard.standardctl import doctor, drift


def _seed_common(root: Path) -> None:
    for p in ['standard.yml', 'apm.yml', 'apm.lock.yaml', '.copier-answers.yml']:
        (root / p).write_text('x: y\n', encoding='utf-8')
    (root / 'standard.yml').write_text('profile: ts-fullstack\n', encoding='utf-8')
    (root / 'apps/web').mkdir(parents=True)
    (root / 'apps/api').mkdir(parents=True)
    (root / 'packages/api-contract').mkdir(parents=True)


def test_doctor_runtime_matrix_requirements() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _seed_common(root)

        # codex runtime
        assert doctor(root, 'codex') == 1
        (root / '.codex').mkdir()
        assert doctor(root, 'codex') == 0

        # claude runtime
        assert doctor(root, 'claude') == 1
        (root / '.claude.instructions.md').write_text('ok\n', encoding='utf-8')
        assert doctor(root, 'claude') == 0

        # dual runtime
        assert doctor(root, 'dual') == 0


def test_drift_runtime_matrix_command_selection(monkeypatch) -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        calls: list[list[str]] = []

        def fake_run(cmd: list[str], cwd: Path) -> tuple[int, str]:
            calls.append(cmd)
            return 0, 'ok'

        monkeypatch.setattr('scripts.standard.standardctl.run_cmd', fake_run)

        assert drift(root, 'claude') == 0
        claude_cmds = [' '.join(c) for c in calls]
        assert any('pnpm docs:verify' in c for c in claude_cmds)
        assert not any('pnpm api:generate --check' in c for c in claude_cmds)

        calls.clear()
        assert drift(root, 'codex') == 0
        codex_cmds = [' '.join(c) for c in calls]
        assert any('pnpm docs:verify' in c for c in codex_cmds)
        assert any('pnpm api:generate --check' in c for c in codex_cmds)
