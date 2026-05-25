import dash
import pandas as pd
from dash import html
from dash import dcc
from dash import Input
from dash import Output
import plotly.express as px

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
    dcc.Dropdown(id ="filtro_turno", options = [{"label":"Diurno", "value": "DIURNO"},
                                                {"label":"Noturno", "value":"NOTURNO"}],
                 value = ["DIURNO"],
                 multi = True),
    dcc.Dropdown(id = "dia_semana", options = [{"label":"Segunda", "value": "seg"},
                                               {"label":"Terca", "value": "ter"},
                                               {"label":"Quarta", "value": "qua"},
                                               {"label":"Quinta", "value": "qui"},
                                               {"label":"Sexta", "value": "sex"},
                                               {"label":"Sabado", "value": "sab"}],
                 value = ["seg","qua","sex"],
                 multi = True),
    dcc.DatePickerRange(id = "filtro_data",
                        start_date = "2025-05-20",
                        end_date = "2025-06-20"),
    dcc.Graph(id = "grafico")
    ])

@app.callback(Output("grafico", "figure"),
              Input("filtro_turno", "value"),
              Input("dia_semana", "value"),
              Input("filtro_data", "start_date"),
              Input("filtro_data", "end_date"))

def atualizar(turno, dia_semana, data_ini, data_fin):
    return gerar_grafico(turno, dia_semana, data_ini, data_fin)

if __name__ == "__main__":
    app.run(debug=True)
