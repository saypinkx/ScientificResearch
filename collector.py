import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os


class DataManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def load_from_excel(self, file: str):
        data = pd.read_excel(file, header=0)
        return data

    def loaf_from_csv(self, file: str):
        data = pd.read_csv(file, header=0)
        return data

    def create_data_for_j(self, x, y, z, inclination, md_vertical, md_inclined, azimuth, intensity):
        count_angle = inclination / intensity
        count_line = count_angle
        one_line = 10
        data = [dict(md=z, inclination=0, azimuth=0, x=x, y=y, z=z), dict(md=md_vertical + z, inclination=0, azimuth=0)]
        md = md_vertical + z
        for i in range(1, int(count_line + 1)):
            md += one_line
            data.append(dict(md=md, inclination=i * intensity, azimuth=azimuth))
        data.append(dict(md=md + md_inclined, inclination=inclination, azimuth=azimuth))
        df = pd.DataFrame(data)
        df.to_excel(f"{self.base_dir}/types/j.xlsx", index=False)
        return data

    def create_data_for_h(self, x, y, z, inclination, md_vertical, md_inclined, azimuth, intensity):
        count_angle = inclination / intensity
        count_line = count_angle
        one_line = 10
        data = [dict(md=z, inclination=0, azimuth=0, x=x, y=y, z=z), dict(md=md_vertical + z, inclination=0, azimuth=0)]
        md = md_vertical + z
        for i in range(1, int(count_line + 1)):
            md += one_line
            data.append(dict(md=md, inclination=i * intensity, azimuth=azimuth))
        data.append(dict(md=md + md_inclined, inclination=inclination, azimuth=azimuth))
        df = pd.DataFrame(data)
        df.to_excel(f"{self.base_dir}/types/h.xlsx", index=False)
        return data

    def create_data_for_v(self, x, y, z, md):
        data = [dict(md=z, inclination=0, azimuth=0, x=x, y=y, z=z), dict(md=md + z, inclination=0, azimuth=0)]
        df = pd.DataFrame(data)
        df.to_excel(f"{self.base_dir}/types/v.xlsx")

    def create_data_for_s(self, md_vertical: float, intensity_up: float, md_drop: float, x: float,
                          y: float, inclination: float, tangent_angle: float,
                          azimuth: float, z: float, intensity_down: float):
        count_angle_inclination = inclination / intensity_up
        count_line_inclination = count_angle_inclination
        one_line_inclination = 10
        data = [dict(md=z, inclination=0, azimuth=0, x=x, y=y, z=z), dict(md=md_vertical + z, inclination=0, azimuth=0)]
        md = md_vertical + z
        for i in range(1, int(count_line_inclination + 1)):
            md += one_line_inclination
            data.append(dict(md=md, inclination=i * intensity_up, azimuth=azimuth))

        count_angle_tangent = tangent_angle / intensity_up
        count_line_tangent = count_angle_tangent
        one_line_tangent = 10
        for i in range(1, int(count_line_tangent + 1)):
            md += one_line_tangent
            data.append(dict(md=md, inclination=inclination - i * intensity_down, azimuth=azimuth))
        data.append(dict(md=md+md_drop, inclination=0, azimuth=azimuth))
        df = pd.DataFrame(data)
        df.to_excel(f"{self.base_dir}/types/s.xlsx", index=False)

    def create_data_for_ellipse(self, file):
        pass


    def handler(self, data: pd.DataFrame):
        md = data['md']
        inclination = data['inclination']
        azimuth = data['azimuth']
        return md, inclination, azimuth
