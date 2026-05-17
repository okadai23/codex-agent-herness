from pathlib import Path


def test_pm_skill_and_agents_exist() -> None:
    root = Path(__file__).resolve().parents[2]
    required_paths = [
        root / 'template/.agents/skills/pm-prd-kit/SKILL.md',
        root / 'template/.agents/skills/pm-prd-kit/templates/prd-template.md',
        root / 'template/.agents/skills/pm-prd-kit/checklists/prd-quality-checklist.md',
        root / 'template/.codex/agents/pm-orchestrator.md',
        root / 'template/.codex/agents/subagents/pm-prd-researcher.md',
        root / 'template/.codex/agents/subagents/pm-prd-writer.md',
        root / 'template/.codex/agents/subagents/pm-prd-critic.md',
    ]
    missing = [str(p) for p in required_paths if not p.exists()]
    assert not missing, f'missing template assets: {missing}'
