from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .data import energy_df

router = APIRouter()

@router.get("/contract")
def get_contract_data():
    # pivot table 형태로 변환: 연도를 index, 시도구분을 columns, 용량이 값
    pivot_df = energy_df.pivot(index='연도', columns='시도구분', values='용량').fillna(0)

    # index인 연도를 컬럼명 year로 변환
    pivot_df.reset_index(inplace=True)
    pivot_df.rename(columns={'연도': 'year'}, inplace=True)

    # pandas dataframe -> dict 리스트 변환
    result = pivot_df.to_dict(orient='records')

    return JSONResponse(content=result)