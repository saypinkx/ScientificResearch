from collector import DataManager
from painter import PaintManager
import os


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

    def get_manual_trajectory_xy(self):
        filenames = os.listdir(self.folder_path)
        nodes = []
        for filename in filenames:
            if filename.endswith(".xlsx"):
                file_path = os.path.join(self.folder_path, filename)
                nodes.append(self.dater.load_from_excel(file_path))
        fig = self.painter.draw_position_wells(nodes=nodes)
        return fig

    def get_type_trajectory_3D(self, type, true_size):
        filepath = f'{self.base_dir}/types/{type}.xlsx'
        node = self.dater.load_from_excel(filepath)
        nodes = []
        nodes.append(node)
        fig = self.painter.draw_trajectory_wells(nodes=nodes, true_size=true_size)
        return fig

    def get_type_trajectory_xy(self, type):
        filepath = f'{self.base_dir}/types/{type}.xlsx'
        node = self.dater.load_from_excel(filepath)
        nodes = []
        nodes.append(node)
        fig = self.painter.draw_position_wells(nodes=nodes)
        return fig

    # def create_j_trajectory(self, x, y, z, inclination, md_vertical, md_inclined, azimuth):
    #     node = self.dater.create_data_for_j(x, y, md_vertical, md_inclined, inclination, azimuth)
