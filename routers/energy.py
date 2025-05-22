from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .data import df_self  

router = APIRouter()

@router.get("/energy")
def get_energy_data():
    data_2023 = df_self[df_self["연도"] == 2023]
    grouped = data_2023[["태양광", "풍력", "수력", "해양", "바이오", "재생폐기물"]].sum()

    result = [
        {"name": "태양광", "value": int(grouped["태양광"])},
        {"name": "풍력", "value": int(grouped["풍력"])},
        {"name": "수력", "value": int(grouped["수력"])},
        {"name": "해양", "value": int(grouped["해양"])},
        {"name": "바이오", "value": int(grouped["바이오"])},
        {"name": "재생폐기물", "value": int(grouped["재생폐기물"])},
    ]

    return JSONResponse(content=result)
