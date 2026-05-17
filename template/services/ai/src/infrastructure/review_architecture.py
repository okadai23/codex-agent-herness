from pathlib import Path

FORBIDDEN_IN_DOMAIN = ("fastapi", "openai", "anthropic")


def main() -> int:
    root = Path(__file__).resolve().parents[2] / "domain"
    violations: list[str] = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for keyword in FORBIDDEN_IN_DOMAIN:
            if keyword in text:
                violations.append(f"{path}: contains forbidden dependency '{keyword}'")
    if violations:
        print("\n".join(violations))
        return 1
    print("architecture boundary check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
