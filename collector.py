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

    def create_data_for_j(self, x, y, z, inclination, md_vertical, md_inclined, azimuth, md_angle):
        one_angle = inclination / 5
        count_line = inclination / one_angle
        one_line = md_angle / count_line
        data = [dict(md=z, inclination=0, azimuth=0, x=x, y=y, z=z), dict(md=md_vertical+z, inclination=0, azimuth=0)]
        md = md_vertical + z
        for i in range(1, int(count_line+1)):
            md += one_line
            data.append(dict(md=md, inclination=i*one_angle, azimuth=azimuth))
        data.append(dict(md=md+md_inclined, inclination=inclination, azimuth=azimuth))
        df = pd.DataFrame(data)
        df.to_excel(f"{self.base_dir}/types/j.xlsx", index=True)
        return data

    def create_data_for_v(self, x, y, z, md):
        data = [dict(md=z, inclination=0, azimuth=0, x=x, y=y, z=z), dict(md=md+z, inclination=0, azimuth=0)]
        df = pd.DataFrame(data)
        df.to_excel(f"{self.base_dir}/types/v.xlsx")

    def handler(self, data: pd.DataFrame):
        md = data['md']
        inclination = data['inclination']
        azimuth = data['azimuth']
        return md, inclination, azimuth
