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

    def draw_trajectory_wells(self, nodes: list, true_size: bool):
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
        md, azimuth, inclination, x_start, y_start, z_start = data['md'], data['azimuth'], data['inclination'], data[
            'x'], data['y'], data['z']
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

    def draw_position_wells_xy(self, nodes: list):
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

    def draw_position_wells_yz(self, nodes: list):
        fig = go.Figure()
        for i in range(len(nodes)):
            node = nodes[i]
            x, y, z = self.get_coords(node)
            fig.add_trace(
                go.Scatter(x=y, y=z, name=f'Позиция скважины {i + 1} на Y-Z плоскости', mode='lines+markers'))
        # scene = dict(xaxis=dict(title='X (м)'),
        #              yaxis=dict(title='Y (м)'))
        fig.update_xaxes(title_text="Z (м)")
        fig.update_yaxes(title_text="Y (м)")

        fig.update_layout(title='Позиция скважины на Y-Z плоскости')
        return fig

    def draw_position_wells_xz(self, nodes: list):
        fig = go.Figure()
        for i in range(len(nodes)):
            node = nodes[i]
            x, y, z = self.get_coords(node)
            fig.add_trace(
                go.Scatter(x=x, y=z, name=f'Позиция скважины {i + 1} на X-Z плоскости', mode='lines+markers'))
        # scene = dict(xaxis=dict(title='X (м)'),
        #              yaxis=dict(title='Y (м)'))
        fig.update_xaxes(title_text="x (м)")
        fig.update_yaxes(title_text="z (м)")

        fig.update_layout(title='Позиция скважины на X-Z плоскости')
        return fig

    def draw_trajectory_wells_with_ellipse(self, data: pd.DataFrame, true_size: bool):
        x, y, z = self.get_coords(data)
        x0, y0, x1, y1, md_ellipse, mean_z, vector_n, vector_u, vector_v, semi_minor_axis, semi_major_axis, mean_x, mean_y = self.get_coords_for_ellipse(
            data)
        e = self.ellipse(x0=x0, y0=y0, x1=x1, y1=y1, md_ellipse=md_ellipse, mean_z=mean_z, vector_n=vector_n,
                         vector_u=vector_u, vector_v=vector_v, semi_minor_axis=semi_minor_axis,
                         semi_major_axis=semi_major_axis, mean_x=mean_x, mean_y=mean_y)

        print(data)
        fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='lines', name='Траектория 1')])
        fig.add_trace(e)
        scene = dict(xaxis=dict(title='X (м)'),
                     yaxis=dict(title='Y (м)'),
                     zaxis=dict(title='TVD (м)'))

        if true_size:
            for key in scene:
                scene[key].update(range=[z[-1], -z[-1]])
        print(z[-1])

        fig.update_layout(title='Траектория скважины',
                          scene=scene)
        return fig

    def draw_ellipse(self, data):
        x, y, z = self.get_coords(data)

        return fig

    def draw_points_for_ellipse(self, nodes):
        fig = go.Figure()
        for i in range(len(nodes)):
            node = nodes[i]
            x, y, z = self.get_coords(node)
            fig.add_trace(
                go.Scatter(x=x, y=y, name=f'Позиция скважины {i + 1} на X-Y плоскости', mode='lines+markers'))

    def get_coords_for_ellipsev1(self, data: pd.DataFrame):
        # Извлечение координат
        md, azimuth, inclination, x_start, y_start, z_start = data['md'], data['azimuth'], data['inclination'], data[
            'x'], data['y'], data['z']
        d_azimuth, d_inclination, correlation, md_ellipse = data['d_azimuth'], data['d_inclination'], data[
            'correlation'], \
            data['md_ellipse']
        azimuth_rad, inclination_rad = np.deg2rad(azimuth), np.deg2rad(inclination)
        d_azimuth, d_inclination = np.deg2rad(d_azimuth)[0], np.deg2rad(d_inclination)[0]
        correlation = correlation[0]
        md_ellipse = md_ellipse[0]

        x, y, z, std_x, std_y = np.zeros_like(md), np.zeros_like(md), np.zeros_like(md), np.zeros_like(
            md), np.zeros_like(md)
        x[0], y[0], z[0] = x_start[0], y_start[0], z_start[0]
        count_positions = len(md)

        for i in range(1, count_positions):
            delta_md = -(md[i] - md[i - 1])
            delta_x, delta_y, delta_z = delta_md * np.sin(inclination_rad[i]) * np.cos(
                azimuth_rad[i]), delta_md * np.sin(inclination_rad[i]) * np.sin(azimuth_rad[i]), delta_md * np.cos(
                inclination_rad[i])
            x[i], y[i], z[i] = x[i - 1] + delta_x, y[i - 1] + delta_y, z[i - 1] + delta_z
            std_x[i], std_y[i] = std_x[i - 1] + delta_md * np.sin(d_inclination) * np.cos(
                d_azimuth), std_y[i - 1] + delta_md * np.sin(d_inclination) * np.sin(d_azimuth)
            if md[i] >= md_ellipse:
                vector_v = np.array([x[i] - x[i - 1], y[i] - y[i - 1], z[i] - z[i - 1]])
                vector_u = np.array([0, 1, 0])

                vector_n = np.cross(vector_v, vector_u)
                mean_z = z[i]
                mean_x = x[i]
                mean_y = y[i]
                std_x = std_x[i]
                std_y = std_y[i]
                cov_matrix = np.array([[std_x * 2, correlation * std_x * std_y],
                                       [correlation * std_x * std_y, std_y * 2]])

                # Вычисление собственных значений и собственных векторов
                eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

                # Определение углов и полуосей эллипса
                angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
                semi_major_axis = abs(eigenvalues[0]) ** 0.5
                semi_minor_axis = abs(eigenvalues[1]) ** 0.5

                x0 = mean_x - semi_major_axis
                y0 = mean_y - semi_minor_axis
                x1 = mean_x + semi_major_axis
                y1 = mean_y + semi_minor_axis
                return x0, y0, x1, y1, md_ellipse, mean_z, vector_n, vector_u, vector_v, semi_minor_axis, semi_major_axis, mean_x, mean_y
        return None

    def draw_ellipse_2D(self, data):
        x0, y0, x1, y1, md_ellipse, mean_z, vector_n, vector_u, vector_v, semi_minor_axis, semi_major_axis, mean_x, mean_y = self.get_coords_for_ellipse(
            data)
        fig = go.Figure()

        # Добавление эллипса
        fig.add_shape(
            type="circle",
            xref="x",
            yref="y",
            x0=x0,
            y0=y0,
            x1=x1,
            y1=y1,
            fillcolor="rgba(255, 0, 0, 0.2)",
            line_color="red",
            opacity=0.5,
            name=f"",
        )

        # Настройка осей
        fig.update_layout(
            xaxis_title="X",
            yaxis_title="Y",
            title=f"  Размеры эллипса неопределенности на xy",
            showlegend=True,
            autosize=False,
            width=600,
            height=400, )
        fig.update_xaxes(range=[x0 - x1 // 2, x1 + x1 // 2])
        fig.update_yaxes(range=[y0 - y1 // 2, y1 + y1 // 2])
        return fig

    def ellipse(self, x0, y0, x1, y1, md_ellipse, mean_z, vector_n, vector_u, vector_v, semi_minor_axis,
                semi_major_axis, mean_x, mean_y):

        a = semi_major_axis  # Большая полуось
        b = semi_minor_axis  # Малая полуось
        n = vector_n
        u = vector_u
        v = vector_v

        # Параметрические уравнения эллипса в плоскости
        theta = np.linspace(0, 2 * np.pi, 100)
        x = a * np.cos(theta)
        y = b * np.sin(theta)

        # Перевод в систему координат, связанную с плоскостью
        # Для этого нужно найти матрицу поворота
        # Матрица поворота должна повернуть ось X в направлении n
        # и ось Y в направлении, ортогональном n и v
        # В этом примере для упрощения возьмем u = (0, 1, 0)
        # и найдем вектор w, ортогональный n и u
        w = np.cross(n, v)

        # Матрица поворота
        R = np.array([
            [n[0] / np.linalg.norm(n), w[0] / np.linalg.norm(w), u[0] / np.linalg.norm(u)],
            [n[1] / np.linalg.norm(n), w[1] / np.linalg.norm(w), u[1] / np.linalg.norm(u)],
            [n[2] / np.linalg.norm(n), w[2] / np.linalg.norm(w), u[2] / np.linalg.norm(u)]
        ])

        # Применить поворот к точкам эллипса
        x_rot = x * R[0, 0] + y * R[1, 0]
        y_rot = x * R[0, 1] + y * R[1, 1]
        z_rot = x * R[0, 2] + y * R[1, 2]

        # Смещение эллипса в точку P
        x_rot += mean_x
        y_rot += mean_y
        z_rot += mean_z

        # Построение эллипса
        fig = go.Scatter3d(x=x_rot, y=y_rot, z=z_rot, mode='lines', name='Эллипс неопределенности')
        return fig

    def get_coords_for_ellipse(self, data: pd.DataFrame):
        # Извлечение координат
        md, azimuth, inclination, x_start, y_start, z_start = data['md'], data['azimuth'], data['inclination'], data[
            'x'], data['y'], data['z']
        d_azimuth, d_inclination, correlation, md_ellipse = data['d_azimuth'], data['d_inclination'], data[
            'correlation'], \
            data['md_ellipse']
        azimuth_rad, inclination_rad = np.deg2rad(azimuth), np.deg2rad(inclination)
        d_azimuth, d_inclination = np.deg2rad(d_azimuth)[0], np.deg2rad(d_inclination)[0]
        correlation = correlation[0]
        md_ellipse = md_ellipse[0]

        x, y, z, std_x, std_y = np.zeros_like(md), np.zeros_like(md), np.zeros_like(md), np.zeros_like(
            md), np.zeros_like(md)
        x[0], y[0], z[0] = x_start[0], y_start[0], z_start[0]
        count_positions = len(md)

        for i in range(1, count_positions):
            delta_md = -(md[i] - md[i - 1])
            delta_x, delta_y, delta_z = delta_md * np.sin(inclination_rad[i]) * np.cos(
                azimuth_rad[i]), delta_md * np.sin(inclination_rad[i]) * np.sin(azimuth_rad[i]), delta_md * np.cos(
                inclination_rad[i])
            x[i], y[i], z[i] = x[i - 1] + delta_x, y[i - 1] + delta_y, z[i - 1] + delta_z
            d_inclination = ((d_inclination ** 2 * (i + 1))) ** 0.5
            d_azimuth = ((d_azimuth ** 2 * (i + 1))) ** 0.5
            std_x[i], std_y[i] = std_x[i - 1] + abs(delta_md * np.sin(d_inclination) * np.cos(
                d_azimuth)), std_y[i - 1] + abs(delta_md * np.sin(d_inclination) * np.sin(d_azimuth))
            if md[i] >= md_ellipse:
                vector_v = np.array([x[i] - x[i - 1], y[i] - y[i - 1], z[i] - z[i - 1]])
                vector_u = np.array([0, 1, 0])

                vector_n = np.cross(vector_v, vector_u)
                mean_z = z[i]
                mean_x = x[i]
                mean_y = y[i]
                std_x = std_x[i]
                std_y = std_y[i]

                # semi_major_axis = mean_x + std_x
                # semi_minor_axis = mean_y + std_y
                semi_major_axis = std_x
                semi_minor_axis = std_y

                x0 = mean_x - semi_major_axis
                y0 = mean_y - semi_minor_axis
                x1 = mean_x + semi_major_axis
                y1 = mean_y + semi_minor_axis
                return x0, y0, x1, y1, md_ellipse, mean_z, vector_n, vector_u, vector_v, semi_minor_axis, semi_major_axis, mean_x, mean_y
        return None
