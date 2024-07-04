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
from dashboards.h import layout
dash_app = dash.Dash(__name__,
                     requests_pathname_prefix='/dashboard/j/', title='J')

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

dash_app.layout = layout

@dash_app.callback(dash.Output('body-div', 'children'), dash.Input('show-secret', 'n_clicks'))
def update_output(n_clicks):
    if n_clicks is None:
        return dcc.Graph(figure=handler.get_type_trajectory_3D(true_size=0, type='j'), id='3d'), dcc.Graph(
            figure=handler.get_type_trajectory_xy(type='j'))
    else:
        return dcc.Graph(figure=handler.get_type_trajectory_3D(true_size=1, type='j'), id='3d'), dcc.Graph(
            figure=handler.get_type_trajectory_xy(type='j'))



@dash_app.callback(
    dash.Output("download-excel", "data"),
    [dash.Input('download-button', 'n_clicks')],
    prevent_initial_call=True
)
def update_download(n_clicks):
    # base64_data = handler.get_excel(type='j')
    if n_clicks > 0:
        df = handler.get_dataframe(type='j')
        return dcc.send_data_frame(df.to_excel, filename="j.xlsx", index=False
                                   )
    return None

