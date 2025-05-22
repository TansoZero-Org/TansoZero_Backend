import pandas as pd
import numpy as np

df_self = pd.read_csv("./data/자립도_분석_결합_파일.csv")
df_contact = pd.read_csv("./data/신재생에너지_계약_현황_목록_전처리.csv")
df_gen = pd.read_csv("./data/발전설비_연료원별_전처리.csv")
df_market = pd.read_csv("./data/전력거래_시장참여설비용량_전처리.csv")

df_gen['기간'] = pd.to_datetime(df_gen['기간'])
df_market['기간'] = pd.to_datetime(df_market['기간'])
df_market['연도'] = df_market['기간'].dt.year

energy_df=df_contact
replace_dict = {
    '강원특별자치도': '강원',
    '경기도': '경기',
    '경상북도': '경북',
    '경상남도': '경남',
    '전라북도': '전북',
    '전라남도': '전남',
    '전북특별자치도': '전북',
    '충청북도': '충북',
    '충청남도': '충남',
    '제주특별자치도': '제주',
    '서울특별시': '서울',
    '부산광역시': '부산',
    '대구광역시': '대구',
    '인천광역시': '인천',
    '광주광역시': '광주',
    '대전광역시': '대전',
    '울산광역시': '울산',
    '세종특별자치시': '세종'
}

energy_df['시도구분'] = energy_df['지역구분'].replace(replace_dict)
energy_df= energy_df.groupby(['연도', '시도구분'])['용량'].sum().reset_index()

energy_df = energy_df.groupby(['연도', '시도구분'])['용량'].sum().reset_index()

energy_df['용량'] = pd.to_numeric(energy_df['용량'], errors='coerce')
energy_df['용량'] = pd.to_numeric(energy_df['용량'], errors='coerce')  
energy_df['용량'] = energy_df['용량'].round(3)  