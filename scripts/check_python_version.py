"""Fail when a file declares a Python version different from .python-version (CI-12).

The runtime version is declared once in .python-version. Some tools cannot read that file, so they
keep their own copy; this script makes sure every copy agrees. Standard library only.

Usage: python scripts/check_python_version.py [repo_root]
"""
import re
import sys
from pathlib import Path

# (file, regex whose first group is the version, how the version is written there)
DECLARATIONS = [
    ('Dockerfile', r'^ARG PYTHON_VERSION=(\S+)$', 'dotted'),
    ('docker-compose.yaml', r'PYTHON_VERSION:-([0-9.]+)\}', 'dotted'),
    ('.circleci/config.yml', r'^  python-version:\n(?:    .*\n)*?    default: "([^"]+)"', 'dotted'),
    ('.devcontainer/docker-compose.yml', r'^\s+VARIANT: "?([0-9.]+)"?\s*$', 'dotted'),
    ('.devcontainer/Dockerfile', r'^ARG VARIANT=(\S+)$', 'dotted'),
    ('ruff.toml', r'^target-version = "py(\d+)"', 'compact'),
]

# Hard-coded versions that would bypass the single source.
FORBIDDEN = [
    ('Dockerfile', r'^FROM python:\d', 'FROM must use ${PYTHON_VERSION}'),
    ('.circleci/config.yml', r'^\s+tag: "?\d', 'executor tags must use << pipeline.parameters.python-version >>'),
    ('.devcontainer/docker-compose.yml', r'^\s+VARIANT: \d', 'quote the version: YAML reads 3.10 as 3.1'),
]


def check(root: Path) -> list:
    errors = []
    expected = (root / '.python-version').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+', expected):
        return [f'.python-version: expected MAJOR.MINOR, found {expected!r}']
    compact = expected.replace('.', '')

    for file, pattern, style in DECLARATIONS:
        path = root / file
        if not path.exists():
            errors.append(f'{file}: missing')
            continue
        found = re.findall(pattern, path.read_text(), flags=re.MULTILINE)
        if not found:
            errors.append(f'{file}: no Python version declaration matching {pattern!r}')
        want = expected if style == 'dotted' else compact
        errors.extend(f'{file}: declares {value}, .python-version says {want}' for value in found if value != want)

    for file, pattern, reason in FORBIDDEN:
        text = (root / file).read_text()
        for number, line in enumerate(text.splitlines(), start=1):
            if re.search(pattern, line):
                errors.append(f'{file}:{number}: {reason}: {line.strip()}')

    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    errors = check(root)
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print(f'Python version {(root / ".python-version").read_text().strip()} is declared consistently')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
