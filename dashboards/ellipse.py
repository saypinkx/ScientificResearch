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
                     requests_pathname_prefix='/dashboard/ellipse/', title='Ellipse')

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
    html.Div(id='body-div', style={'textAlign': 'center', 'display': 'flex',
    'flex-direction': 'column',
    'align-items': 'center'})])

dash_app.layout = layout


@dash_app.callback(dash.Output('body-div', 'children'), dash.Input('show-secret', 'n_clicks'))
def update_output(n_clicks):
    if n_clicks is None:
        return dcc.Graph(figure=handler.get_ellipse_trajectory(true_size=0), id='3d'), dcc.Graph(
            figure=handler.get_ellipse_2D())
    else:
        return dcc.Graph(figure=handler.get_ellipse_trajectory(true_size=1), id='3d'), dcc.Graph(
            figure=handler.get_ellipse_2D())
