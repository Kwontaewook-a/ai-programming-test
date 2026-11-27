# test_analysis.py
import pandas as pd
from pathlib import Path
from analysis import 정제, 반별평균

데이터_폴더 = Path(__file__).parent
본 = 정제(pd.read_csv(데이터_폴더 / "scores_2026.csv"))
미니 = 정제(pd.read_csv(데이터_폴더 / "mini.csv"))

def test_정제하면_100행이_남는다():        # ① 행 수 보존
    assert len(본) == 100

def test_반은_두_종류만_남는다():         # ① 행 수 보존
    assert sorted(본["반"].unique()) == ["1반", "2반"]

def test_그룹합이_전체합과_같다():        # ② 합계 일치
    assert 본.groupby("반")["점수"].sum().sum() == 본["점수"].sum()

def test_손계산과_일치한다():             # ③ 손계산 대조
    assert 반별평균(미니)["1반"] == 80.0