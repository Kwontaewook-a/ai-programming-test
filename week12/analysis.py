import pandas as pd

from pathlib import Path
import pandas as pd

def 정제(df):
    df = df.copy()

    # 1. 점수가 비어 있는 행 삭제
    df = df.dropna(subset=["점수"])
    print(f"점수 결측 제거 후: {len(df)}행")

    # 2. 모든 열이 같은 중복 행 제거
    df = df.drop_duplicates()
    print(f"중복 제거 후: {len(df)}행")

    # 3. 반과 과목 앞뒤 공백 제거
    df["반"] = df["반"].astype("string").str.strip()
    df["과목"] = df["과목"].astype("string").str.strip()
    print(f"공백 제거 후: {len(df)}행")

    # 4. 0~100 범위의 정수 점수만 남김
    점수 = pd.to_numeric(df["점수"], errors="coerce")
    유효점수 = 점수.between(0, 1000) & 점수.mod(1).eq(0)
    df = df.loc[유효점수].copy()
    df["점수"] = 점수.loc[유효점수].astype(int)
    print(f"유효 점수 필터링 후: {len(df)}행")

    return df


def 반별평균(df):
    return df.groupby("반")["점수"].mean()


if __name__ == "__main__":
    csv_path = Path(__file__).parent / "scores_2026.csv"

    df = pd.read_csv(csv_path)
    정제된_df = 정제(df)

    print("\n반별 점수 평균:")
    반별_평균 = 정제된_df.groupby("반", as_index=False)["점수"].mean()
    print(반별_평균)

    print("\n과목별·반별 점수 평균:")
    과목_반별_평균 = 정제된_df.groupby(
        ["과목", "반"], as_index=False
    )["점수"].mean()
    print(과목_반별_평균)

    print("\n반별 점수 통계:")
    반별_통계 = (
        정제된_df.groupby("반")["점수"]
        .agg(["count", "mean", "median", "max"])
        .round(2)
        .rename(
            columns={
                "count": "개수",
                "mean": "평균",
                "median": "중앙값",
                "max": "최댓값",
            }
        )
        .reset_index()
    )
    print(반별_통계)

    수학_df = 정제된_df[정제된_df["과목"] == "수학"]
    print(f"\n수학 행 수: {len(수학_df)}")
    print("\n수학 정제 데이터:")
    print(수학_df.to_string(index=False))

    print("그룹 합의 합:", 정제된_df.groupby("반")["점수"].sum().sum())
    print("전체 합:", 정제된_df["점수"].sum())
    print("그룹 개수의 합:", 정제된_df.groupby("반")["점수"].count().sum())
    print("전체 행 수:", len(정제된_df))
