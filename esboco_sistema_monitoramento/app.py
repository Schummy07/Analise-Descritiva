import funcs as fc
import dash
from dash import html
from dash import dcc
from dash import Input
from dash import Output

app = dash.Dash(__name__)


app.layout = html.Div([
    
    html.Div([html.H1("Mapa Analítico"),
    dcc.Dropdown(id = "Parametro_Operacional", 
                  options = [{"label": "Tonelagem", "value": "producao"},
                             {"label": "Tempo_Coleta", "value": "horas_coleta"},
                             {"label": "Tamanho: km percorrido em coleta", "value": "km_coleta"}, 
                             {"label": "Produtividade: ton/h", "value": "ton/h"},
                             {"label": "Densidade: ton/km", "value": "ton/km"}],
                  value = "producao",
                  multi = False),
    dcc.DatePickerRange(id = "filtro_data",
                        start_date = "2025-05-20",
                        end_date = "2025-06/20"),
    dcc.Dropdown(id = "Turno",
                 options = [{"label": "Noturno", "value": "NOTURNO"},
                            {"label": "Diurno", "value": "DIURNO"}],
                 value = ["DIURNO"],
                 multi = True), 
    dcc.Dropdown(id = "Frequencia",
                 options = [{"label":"Segunda", "value": "seg"},
                            {"label":"Terca", "value": "ter"},
                            {"label":"Quarta", "value": "qua"},
                            {"label":"Quinta", "value": "qui"},
                            {"label":"Sexta", "value": "sex"},
                            {"label":"Sabado", "value": "sáb"}],
                 value = ["seg","ter","qua","qui","sex","sáb","dom"],
                 multi = True)], 
             style = {"justifyContent": "center", "width": "60%" }),
    
    html.Div([dcc.Graph(id = "grafico")], 
             style = {"display": "flex", "justifyContent": "center", "marginTop": "30px", "marginBottom": "50px"})
], 
                      style={
        "display": "flex",
        "flexDirection": "column",   
        "alignItems": "center",      
        "mainHeight": "100vh", 
        "paddingBottom": "50px"
    })

def atualizar(variavel, data_ini, data_fin, turno, dia_semana):
    return fc.mapa_analitico(variavel, data_ini, data_fin, turno, dia_semana)

app.callback(Output("grafico", "figure"),
             Input("Parametro_Operacional", "value"),
             Input("filtro_data", "start_date"),
             Input("filtro_data", "end_date"),
             Input("Turno", "value"),
             Input("Frequencia", "value"))(atualizar)

if __name__ == "__main__":
    app.run(debug=True)