import pandas as pd
import plotly.express as px 
import geopandas as gps

def mapa_analitico(variavel, data_ini, data_fin, turno, dia_semana):
    # coreção da variável para se ajustar ao projeto 
    #variavel = variavel[0]
    
    #importação dos dados
    dados = pd.read_excel("dados.xlsx", sheet_name= "Dados")
    dados["data"] = pd.to_datetime(dados["data"], dayfirst= True)
    mapa = gps.read_file("mapa_atual.geojson")
    
    data_ini = pd.to_datetime(data_ini)
    data_fin = pd.to_datetime(data_fin)
    
    #aplicação dos filtros 
    dados_analise = dados[(dados["data"]>= data_ini) &
                          (dados["data"]<= data_fin) &
                          (dados["turno"].isin(turno)) &
                          (dados["dia_semana"].isin(dia_semana))]
    
    #calculo das médias da variável selecionada para cada setor 
    medias = dados_analise.groupby("setor", as_index = False)[variavel].mean()
    medias["setor"] = [f"0{i}" if i <10 else f"{i}" for i in medias["setor"]]
    
    #aplicação do filtro no arquivo shp 
    mapa_filtro = mapa[mapa["SETOR"].isin(medias["setor"])]
    mapa_plot = mapa_filtro.__geo_interface__
    
    # return mapa_filtro, medias - linha de teste 
    # plot do gráfico georeferenciado 
    fig = px.choropleth_map(
        medias,
        geojson=mapa_plot,
        locations="setor",
        featureidkey="properties.SETOR",
        color= variavel,
        color_continuous_scale="Oranges",
        center = {"lat": -22.39, "lon": -47.577}, 
        zoom = 11, 
        opacity = 0.5)
    
    fig.update_layout(
        margin=dict(l=8, r=0, t=0, b=0), 
        width = 900, 
        height = 900)
    
    return fig
    