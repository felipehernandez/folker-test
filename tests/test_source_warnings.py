"""Guards against source that only warns today and breaks on a newer Python (BUG-10).

An invalid escape sequence such as '\\$' is a DeprecationWarning on 3.10/3.11, a
SyntaxWarning on 3.12+ and is meant to become an error. Pytest only sees it when a module
is compiled fresh (a cached .pyc hides it), so compile every source file explicitly.
"""
import pathlib
import warnings

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCES = sorted(path
                 for directory in ('folker', 'tests', 'example')
                 for path in (ROOT / directory).rglob('*.py'))


def compile_with_warnings_as_errors(source: str, name: str):
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        compile(source, name, 'exec')


def test_the_guard_detects_an_invalid_escape_sequence():
    with pytest.raises((DeprecationWarning, SyntaxWarning, SyntaxError)):
        compile_with_warnings_as_errors("re.findall('\\${x}', text)", '<invalid-escape>')


@pytest.mark.parametrize('path', SOURCES, ids=lambda path: str(path.relative_to(ROOT)))
def test_source_compiles_without_warnings(path):
    compile_with_warnings_as_errors(path.read_text(encoding='utf-8'), str(path))
