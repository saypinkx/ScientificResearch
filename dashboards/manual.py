from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import dash
from painter import PaintManager
from collector import DataManager
from handler import Handler
from dash.exceptions import PreventUpdate
import os

dash_app = dash.Dash(__name__,
                     requests_pathname_prefix='/dashboard/manual/', title='M')

header = dbc.Row(
    dbc.Col(
        [
            html.Div(style={"height": 30}),
            html.H1("Demo", className="text-center"),
        ]
    ),
    className="mb-4",
)
hand = Handler()

# dash_app.layout = [
#     html.Div(children='My First App with Data and a Graph'),
#     dcc.Graph(figure=hand.get_fig_3D(), id='3d')
# ]
# dash_app.layout = html.Div(children=[
#     html.H1(children="Dash App"),
#
#     dcc.Graph(id='my-graph'),
# ])

#
# @dash_app.callback(
#     dash.Output('my-graph', 'figure'),
#     [dash.Input('tf1', 'children')]
# )
# def update_graph(file):
#     fig = dcc.Graph(figure=hand.get_fig_3D(), id='3d')
#     return fig

dash_app.layout = html.Div([
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

], style={'textAlign': 'center'})


@dash_app.callback(dash.Output('body-div', 'children'), dash.Input('show-secret', 'n_clicks'))
def update_output(n_clicks):
    if n_clicks is None:
        return dcc.Graph(figure=hand.get_manual_trajectory_3D(true_size=0), id='3d'), dcc.Graph(
            figure=hand.get_manual_trajectory_xy())

    else:
        return dcc.Graph(figure=hand.get_manual_trajectory_3D(true_size=1), id='3d'), dcc.Graph(
            figure=hand.get_manual_trajectory_xy())

#
# @dash_app.callback(dash.Output('body-div2', 'children'), dash.Input('xy', 'n_clicks'))
# def update_output2(n_clicks):
#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         return dcc.Graph(figure=hand.get_trajectory_xy())
