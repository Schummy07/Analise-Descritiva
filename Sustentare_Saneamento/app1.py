import dash
import pandas as pd
from dash import html
from dash import dcc
from dash import Input
from dash import Output
import plotly.express as px
import seaborn as sns 

app = dash.Dash(__name__)


def gerar_grafico(turno, dia_semana, data_ini, data_fin):
    df = pd.read_excel("dados.xlsx", sheet_name = "Dados_gráficos ")
    data = df[(df["Data"] >= data_ini) & (df["Data"] <= data_fin) & (df["Dia_semana"].isin(dia_semana)) & (df["Turno"].isin(turno))]
    data["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
    fig = px.line(data, x="Data", y="Produção_ton", color = "Setor")
    fig.update_xaxes(nticks=10)
    return fig


app.layout = html.Div([
    html.H1("Série histórica"), 
    
    html.Div([html.H4("filtro_de_turno", style = {"marginBottom": "5px"}),
              dcc.Checklist(id ="filtro_turno", 
                 options = ["DIURNO","NOTURNO"],
                 value = ["DIURNO"],
                 inline = True,
                 style={"width": "400px","fontSize": "14px","justifyContent": "center"})]),
    
    html.Div([html.H4("filtro_de_dia", style = {"marginBottom": "5px"}),
              dcc.Checklist(id = "dia_semana", 
                 options = ["seg","ter","qua","qui","sex","sab"],
                 value = ["seg","qua","sex"],
                 inline = True)], 
                 style = {"border": "1px solid black", "marginTop":"30px", "textAlign": "center", "width":"350px"}),
    
    html.Div([html.H4("filtro_de_data"),
              dcc.DatePickerRange(id = "filtro_data",
                        start_date = "2025-05-20",
                        end_date = "2025-06-20")]),
    
    dcc.Graph(id = "grafico")
    ])

app.callback(Output("grafico", "figure"),
              Input("filtro_turno", "value"),
              Input("dia_semana", "value"),
              Input("filtro_data", "start_date"),
              Input("filtro_data", "end_date"))(gerar_grafico)

#def atualizar(turno, dia_semana, data_ini, data_fin):
#    return gerar_grafico(turno, dia_semana, data_ini, data_fin)

if __name__ == "__main__":
    app.run(debug=True)