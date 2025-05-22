from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .data import df_gen, df_market
import numpy as np

router = APIRouter()

@router.get("/efficiency")
def get_efficiency_data():
    latest_year = int(df_gen['기간'].dt.year.max())

    renewable_cols = ['태양광', '풍력', '수력', '해양', '바이오', '폐기물']

    # 2. 연간 평균 설비 / 총 발전량
    capacity_data = df_gen[df_gen['기간'].dt.year == latest_year].groupby('지역')[renewable_cols].mean()
    generation_data = df_market[df_market['기간'].dt.year == latest_year].groupby('지역')[renewable_cols].sum()

    # 3. 효율 계산
    capacity_data = capacity_data.replace(0, np.nan)
    efficiency = (generation_data / capacity_data) * 100
    efficiency = efficiency.fillna(0)
    efficiency['평균이용률(%)'] = efficiency.replace(0, np.nan).mean(axis=1).fillna(0)

    # 4. 결과를 Python 기본 타입으로 변환
    result = efficiency['평균이용률(%)'].sort_values(ascending=False).round(2).to_dict()
    result = {k: float(v) for k, v in result.items()}  # numpy 타입 → float 변환

    return JSONResponse(content={"latest_year": latest_year, "efficiency": result})
