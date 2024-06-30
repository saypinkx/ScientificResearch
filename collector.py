import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

class DataManager:
    def load_from_excel(self, file: str):
        data = pd.read_excel(file, header=0)
        return data

    def loaf_from_csv(self, file: str):
        data = pd.read_csv(file, header=0)
        return data

    def handler(self, data: pd.DataFrame):
        md = data['md']
        inclination = data['inclination']
        azimuth = data['azimuth']
        return md, inclination, azimuth
