import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


class PaintManager:
    def draw_trajectory(self, md: pd.Series, inclination: pd.Series, azimuth: pd.Series):
        pass

    # def draw_trajectory_well(self, data: pd.DataFrame, true_size: bool):
    #     x, y, z = self.get_coords(data)
    #     print(data)
    #     fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='lines', name='Траектория 1')])
    #     scene = dict(xaxis=dict(title='X (м)'),
    #                  yaxis=dict(title='Y (м)'),
    #                  zaxis=dict(title='TVD (м)'))
    #
    #     if true_size:
    #         for key in scene:
    #             scene[key].update(range=[z[-1], -z[-1]])
    #     print(z[-1])
    #
    #     fig.update_layout(title='Траектория скважины',
    #                       scene=scene)
    #     return fig

    def draw_trajectory_wells(self, nodes:list, true_size: bool):
        data = []
        for i in range(len(nodes)):
            node = nodes[i]
            x, y, z = self.get_coords(node)
            max_z = abs(z[-1])
            data.append(go.Scatter3d(x=x, y=y, z=z, mode='lines', name=f'Траектория скважины {i + 1}'))
        fig = go.Figure(data=data)
        scene = dict(xaxis=dict(title='X (м)'),
                     yaxis=dict(title='Y (м)'),
                     zaxis=dict(title='TVD (м)'))

        if true_size:
            for key in scene:
                scene[key].update(range=[-max_z, max_z])

        fig.update_layout(title='Траектория скважины',
                          scene=scene)
        return fig

    def get_coords(self, data: pd.DataFrame):
        md, azimuth, inclination, x_start, y_start, z_start = data['md'], data['azimuth'], data['inclination'], data['x'], data['y'], data['z']
        azimuth_rad, inclination_rad = np.deg2rad(azimuth), np.deg2rad(inclination)
        x, y, z = np.zeros_like(md), np.zeros_like(md), np.zeros_like(md)
        x[0], y[0], z[0] = x_start[0], y_start[0], z_start[0]
        count_positions = len(md)

        for i in range(1, count_positions):
            delta_md = -(md[i] - md[i - 1])
            delta_x, delta_y, delta_z = delta_md * np.sin(inclination_rad[i]) * np.cos(
                azimuth_rad[i]), delta_md * np.sin(inclination_rad[i]) * np.sin(azimuth_rad[i]), delta_md * np.cos(
                inclination_rad[i])
            x[i], y[i], z[i] = x[i - 1] + delta_x, y[i - 1] + delta_y, z[i - 1] + delta_z
        return x, y, z

    # def draw_position_well(self, data: pd.DataFrame):
    #     x, y, z = self.get_coords(data)
    #     print(data)
    #     fig = go.Figure()
    #     fig.add_trace(
    #         go.Scatter(x=x, y=y, name='Позиция скважины на X-Y плоскости', mode='lines', line=dict(color='red')))
    #     scene = dict(xaxis=dict(title='X (м)'),
    #                  yaxis=dict(title='Y (м)'))
    #
    #     fig.update_layout(title='Позиция скважины на X-Y плоскости', scene=scene)
    #     return fig

    def draw_position_wells(self, nodes: list):
        fig = go.Figure()
        for i in range(len(nodes)):
            node = nodes[i]
            x, y, z = self.get_coords(node)
            fig.add_trace(
                go.Scatter(x=x, y=y, name=f'Позиция скважины {i + 1} на X-Y плоскости', mode='lines+markers'))
        # scene = dict(xaxis=dict(title='X (м)'),
        #              yaxis=dict(title='Y (м)'))
        fig.update_xaxes(title_text="X (м)")
        fig.update_yaxes(title_text="Y (м)")

        fig.update_layout(title='Позиция скважины на X-Y плоскости')
        return fig
