from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import dash
from painter import PaintManager
from collector import DataManager
from handler import Handler
from dash.exceptions import PreventUpdate
import os
import base64
from io import BytesIO

dash_app = dash.Dash(__name__,
                     requests_pathname_prefix='/dashboard/h/', title='Kaustubh Demo')

header = dbc.Row(
    dbc.Col(
        [
            html.Div(style={"height": 30}),
            html.H1("Demo", className="text-center"),
        ]
    ),
    className="mb-4",
)
handler = Handler()

layout = html.Div([
    html.Button('Нажми сюда, чтобы увидеть настоящие размеры', id='show-secret',
                style={
                    'backgroundColor': '#4CAF50',  # Зеленый цвет фона
                    'color': 'white',  # Белый цвет текста
                    'padding': '15px 32px',  # Отступы
                    'textAlign': 'center',  # Текст по центру
                    'textDecoration': 'none',  # Без подчеркивания
                    'display': 'inline-block',  # Кнопка как в строке
                    'fontSize': '16px',  # Размер шрифта
                    'borderRadius': '5px',  # Закругленные углы
                    'border': 'none',
                    'cursor': 'pointer'}),
    html.Div(id='body-div'),
    # html.Button('Click here to see the content', id='xy'),
    html.Div(children=[
        dcc.Download(id="download-excel"),
        html.Button(
            id='download-button',
            children='Скачать xlsx для построения',
            n_clicks=0,
            style={
                'backgroundColor': '#4CAF50',  # Зеленый цвет фона
                'color': 'white',  # Белый цвет текста
                'padding': '15px 32px',  # Отступы
                'textAlign': 'center',  # Текст по центру
                'textDecoration': 'none',  # Без подчеркивания
                'display': 'inline-block',  # Кнопка как в строке
                'fontSize': '16px',  # Размер шрифта
                'borderRadius': '5px',  # Закругленные углы
                'border': 'none',
                'cursor': 'pointer'}
        )])], style={'textAlign': 'center'})
dash_app.layout =layout

@dash_app.callback(dash.Output('body-div', 'children'), dash.Input('show-secret', 'n_clicks'))
def update_output(n_clicks):
    if n_clicks is None:
        return dcc.Graph(figure=handler.get_type_trajectory_3D(true_size=0, type='h'), id='3d'), dcc.Graph(
            figure=handler.get_type_trajectory_xy(type='h'))
    else:
        return dcc.Graph(figure=handler.get_type_trajectory_3D(true_size=1, type='h'), id='3d'), dcc.Graph(
            figure=handler.get_type_trajectory_xy(type='h'))


@dash_app.callback(
    dash.Output("download-excel", "data"),
    [dash.Input('download-button', 'n_clicks')],
    prevent_initial_call=True
)
def update_download(n_clicks):
    # base64_data = handler.get_excel(type='j')
    if n_clicks > 0:
        df = handler.get_dataframe(type='h')
        return dcc.send_data_frame(df.to_excel, filename="h.xlsx", index=False
                                   )
    return None
