from pathlib import Path
import importlib.util

import pytest


MODULE_PATH = Path(__file__).parent / "week11_files" / "bug3_logic.py"

spec = importlib.util.spec_from_file_location("bug3_logic", MODULE_PATH)
bug3_logic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bug3_logic)

find_max = bug3_logic.find_max
count_pass = bug3_logic.count_pass


def test_find_max_includes_last_score():
    assert find_max([70, 85, 60, 95]) == 95


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ([70, 85, 60, 95], 3),
        ([60, 60, 59], 2),
        ([95, 85, 70], 3),
    ],
)
def test_count_pass_includes_cutoff_score(scores, expected):
    assert count_pass(scores) == expected
