from fastapi import APIRouter
from .data import df_self, df_contact, df_market

router = APIRouter()

@router.get("/dashboard")
def get_self_sufficiency_average():

    #자립도
    avg_self_sufficiency = df_self['자립도(%)'].mean()
    avg_self_sufficiency = round(avg_self_sufficiency, 2)

    # 탄소회피량 - 평균 (현재년도)
    latest_year = df_self['연도'].max()  # 가장 최신 연도 찾기
    avg_carbon_avoidance = df_self[df_self['연도'] == latest_year]['탄소회피량'].mean()
    avg_carbon_avoidance = round(avg_carbon_avoidance, 2)

    # 탄소회피량 - 평균 (전년도)
    prev_year_carbon_avoidance = df_self[df_self['연도'] == (df_self['연도'].max() - 1)]['탄소회피량'].mean()
    prev_year_carbon_avoidance = round(prev_year_carbon_avoidance, 2)

    # 탄소회피량 증가율 계산 (전년 대비 %)
    if prev_year_carbon_avoidance and prev_year_carbon_avoidance != 0:
        carbon_avoidance_growth_rate = ((avg_carbon_avoidance - prev_year_carbon_avoidance) / prev_year_carbon_avoidance) * 100
        carbon_avoidance_growth_rate = round(carbon_avoidance_growth_rate, 2)
    else:
        carbon_avoidance_growth_rate = None

    # 신재생에너지 비율 (현재년도)
    latest_year = df_market['연도'].max()  # 최신 연도
    df_latest = df_market[df_market['연도'] == latest_year]  # 최신 연도 데이터 필터링

    ratio = (df_latest['신재생 합계'].sum() / df_latest['합계'].sum()) * 100
    ratio = round(ratio, 2)


    # 신재생에너지 비율 (전년도)
    prev_year_market = df_market[df_market['연도'] == (df_market['연도'].max() - 1)]
    prev_year_ratio = (prev_year_market['신재생 합계'].sum() / prev_year_market['합계'].sum()) * 100
    prev_year_ratio = round(prev_year_ratio, 2)

    # 신재생에너지 비율 증가율 계산 (전년 대비 %)
    if prev_year_ratio and prev_year_ratio != 0:
        ratio_growth_rate = ((ratio - prev_year_ratio) / prev_year_ratio) * 100
        ratio_growth_rate = round(ratio_growth_rate, 2)
    else:
        ratio_growth_rate = None

    #계약 증가율
    df_yearly = df_contact.groupby("연도")["개수"].sum().reset_index()

    # 누적 합계 계산
    df_yearly["누적계약수"] = df_yearly["개수"].cumsum()

    # 누적계약수 기준 전년 대비 증가율 계산
    df_yearly["증가율(%)"] = df_yearly["누적계약수"].pct_change() * 100
    latest_growth_rate = round(df_yearly["증가율(%)"].iloc[-1], 2)

    return {
    "self_sufficiency": avg_self_sufficiency,
    "avg_carbon_avoidance": avg_carbon_avoidance,
    "carbon_avoidance_growth_rate":carbon_avoidance_growth_rate,
    "ratio": ratio,
    "ratio_growth_rate":ratio_growth_rate,
    "latest_growth_rate":latest_growth_rate
}