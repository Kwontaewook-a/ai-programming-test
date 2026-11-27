from pathlib import Path
import importlib.util

import pytest


cwd = Path.cwd()
MODULE_PATH = next(
    (
        path
        for path in cwd.rglob("load_scores.py")
        if path.parent.name in {"week11", "week11_files"}
    ),
    cwd / "load_scores.py",
)
SPEC = importlib.util.spec_from_file_location("week11_load_scores", MODULE_PATH)
load_scores_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(load_scores_module)
load_scores = load_scores_module.load_scores


def test_header_only_returns_empty_lists(tmp_path):
    csv_path = tmp_path / "header.csv"
    csv_path.write_text("name,score\n", encoding="utf-8")

    assert load_scores(csv_path) == ([], [])


def test_loads_valid_names_scores_and_keeps_duplicates(tmp_path):
    csv_path = tmp_path / "scores.csv"
    csv_path.write_text(
        "name,score\n김철수,95\n이영희,88\n김철수,72\n",
        encoding="utf-8-sig",
    )

    kept, skipped = load_scores(csv_path)

    assert kept == [("김철수", 95), ("이영희", 88), ("김철수", 72)]
    assert skipped == []


def test_accepts_whitespace_and_both_boundary_scores(tmp_path):
    csv_path = tmp_path / "boundaries.csv"
    csv_path.write_text(
        "name,score\n최소, 0 \n최대,100\n일반, 77 \n",
        encoding="utf-8",
    )

    assert load_scores(csv_path) == (
        [("최소", 0), ("최대", 100), ("일반", 77)],
        [],
    )


def test_missing_file_raises_file_not_found_error(tmp_path):
    missing = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(missing)


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ("세열,90,추가", "열 개수가 2가 아님"),
        ("한열만", "열 개수가 2가 아님"),
        (",90", "이름이 비어 있음"),
        ("이름,", "점수가 비어 있음"),
        ("이름,abc", "점수가 정수가 아님"),
        ("이름,88.5", "점수가 정수가 아님"),
        ("이름,-1", "점수가 0~100 밖"),
        ("이름,101", "점수가 0~100 밖"),
    ],
)
def test_invalid_rows_are_skipped_with_reason(tmp_path, row, reason):
    csv_path = tmp_path / "invalid.csv"
    csv_path.write_text(f"name,score\n{row}\n", encoding="utf-8")

    kept, skipped = load_scores(csv_path)

    assert kept == []
    assert skipped == [(2, row, reason)]


def test_blank_line_is_not_recorded_and_line_numbers_include_it(tmp_path):
    csv_path = tmp_path / "blank.csv"
    csv_path.write_text(
        "name,score\n\n김영,80\n잘못,abc\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_path)

    assert kept == [("김영", 80)]
    assert skipped == [(4, "잘못,abc", "점수가 정수가 아님")]
