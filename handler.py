from collector import DataManager
from painter import PaintManager
import os

import base64


class Handler:
    def __init__(self):
        self.dater = DataManager()
        self.painter = PaintManager()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder_path = self.base_dir + '/data'

    def get_manual_trajectory_3D(self, true_size):
        filenames = os.listdir(self.folder_path)
        data = []
        for filename in filenames:
            if filename.endswith(".xlsx"):
                file_path = os.path.join(self.folder_path, filename)
                data.append(self.dater.load_from_excel(file_path))

        fig = self.painter.draw_trajectory_wells(nodes=data, true_size=true_size)
        return fig

    def get_manual_trajectory_2D(self):
        filenames = os.listdir(self.folder_path)
        nodes = []
        for filename in filenames:
            if filename.endswith(".xlsx"):
                file_path = os.path.join(self.folder_path, filename)
                nodes.append(self.dater.load_from_excel(file_path))
        fig_xy = self.painter.draw_position_wells_xy(nodes=nodes)
        fig_xz = self.painter.draw_position_wells_xz(nodes=nodes)
        fig_yz = self.painter.draw_position_wells_yz(nodes=nodes)

        return fig_xy, fig_xz, fig_yz

    def get_type_trajectory_3D(self, type, true_size):
        filepath = f'{self.base_dir}/types/{type}.xlsx'
        node = self.dater.load_from_excel(filepath)
        nodes = []
        nodes.append(node)
        fig = self.painter.draw_trajectory_wells(nodes=nodes, true_size=true_size)
        return fig

    def get_type_trajectory_2D(self, type):
        filepath = f'{self.base_dir}/types/{type}.xlsx'
        node = self.dater.load_from_excel(filepath)
        nodes = []
        nodes.append(node)
        xy, xz, yz = self.painter.draw_position_wells_xy(nodes=nodes), self.painter.draw_position_wells_xz(
            nodes=nodes), self.painter.draw_position_wells_yz(nodes=nodes)

        return xy, xz, yz

    def get_dataframe(self, type):
        df = self.dater.load_from_excel(file=f"{self.base_dir}/types/{type}.xlsx")
        return df

    def get_ellipse_trajectory(self, true_size):
        filepath = f'{self.base_dir}/types/ellipse.xlsx'
        node = self.dater.load_from_excel(filepath)
        fig = self.painter.draw_trajectory_wells_with_ellipse(data=node, true_size=true_size)

        return fig

    def get_ellipse_2D(self):
        filepath = f'{self.base_dir}/types/ellipse.xlsx'
        node = self.dater.load_from_excel(filepath)
        fig = self.painter.draw_ellipse_2D(data=node)
        return fig

    # def create_j_trajectory(self, x, y, z, inclination, md_vertical, md_inclined, azimuth):
    #     node = self.dater.create_data_for_j(x, y, md_vertical, md_inclined, inclination, azimuth)
