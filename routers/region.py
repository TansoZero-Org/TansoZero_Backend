from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import folium
import json
import pandas as pd
from .data import df_self

router = APIRouter()

# geoJSON 파일 로드
file_path = "./data/TL_SCCO_CTPRVN.json"  # Update the file path if necessary

with open(file_path, 'r', encoding='utf-8') as f:
    geo_json_data = json.load(f)

# GeoJSON 구조
properties = [f['properties'] for f in geo_json_data['features']]
geojson_df = pd.DataFrame(properties)

# Define the energy sources
energy_sources = [
    "신재생에너지 합계", '태양광', '풍력', '수력', '해양', '바이오', '재생폐기물', '연료전지', 'IGCC'
]

@router.get("/region/{energy_source}", response_class=HTMLResponse)
def get_region_data(energy_source: str):
    # Check if the energy source is valid
    if energy_source not in energy_sources:
        return HTMLResponse(content="Invalid energy source.", status_code=400)

    center = [36.5, 127.8]  # Center of the map

    # Create map centered on the specified location
    m = folium.Map(location=center, zoom_start=7)

    # Create a choropleth map for the selected energy source
    choropleth = folium.Choropleth(
        geo_data=geo_json_data,
        data=df_self,
        columns=['시도코드', energy_source],
        key_on='feature.properties.CTPRVN_CD',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'전체 연도 시도별 {energy_source} 발전량 합계'
    ).add_to(m)

    # Add GeoJSON tooltip
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['CTP_KOR_NM'], labels=False)
    )

    # Saving map as an HTML file
    map_html = m._repr_html_()  # Folium's method to get HTML string of the map

    return HTMLResponse(content=map_html)
