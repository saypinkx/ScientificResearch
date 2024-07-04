# from collector import DataManager
# from painter import PaintManager
# dater = DataManager()
# data = dater.load_from_excel('data/for_elipse.xlsx')
# # data2 = dater.load_from_excel('data/data.xlsx')
# cat = PaintManager()
# cat.draw_trajectory_wells_with_ellipse(true_size=0, data=data).show()
# cat.draw_trajectory_well(data, true_size=1)

# import numpy as np
# mass = np.empty([0])
# mass = np.append(mass, [2])
# print(mass)


import plotly.graph_objects as go
import numpy as np

# Параметры эллипса
mean_x = 2
mean_y = 3
std_x = 1
std_y = 2
correlation = 0.5

# Вычисление ковариационной матрицы
cov_matrix = np.array([[std_x*2, correlation * std_x * std_y],
                      [correlation * std_x * std_y, std_y*2]])

# Вычисление собственных значений и собственных векторов
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

# Определение углов и полуосей эллипса
angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
semi_major_axis = np.sqrt(eigenvalues[0])
semi_minor_axis = np.sqrt(eigenvalues[1])

# Создание фигуры plotly
fig = go.Figure()
fig.add_trace(go.Surface(
    x=x,
    y=y,
    z=z,
    opacity=0.5,
    colorscale="Viridis",
    showscale=False,
    name="Эллипсоид неопределенности"
))
#
# # Добавляем точку, чтобы обозначить центр
# fig.add_trace(go.Scatter3d(
#     x=[center[0]],
#     y=[center[1]],
#     z=[center[2]],
#     mode="markers",
#     marker=dict(
#         color="blue",
#         size=10
#     ),
#     name="Центр"
# ))
#
# # Настраиваем оси
# fig.update_layout(
#     scene=dict(
#         xaxis_title="X",
#         yaxis_title="Y",
#         zaxis_title="Z"
#     ),
#     title="Эллипсоид неопределенности",
#     showlegend=True,
#     autosize=False,
#     width=800,
#     height=600
# )

# Отображаем график
fig.show()
# # Добавление эллипса
# fig.add_shape(
#     type="circle",
#     xref="x",
#     yref="y",
#     x0=mean_x - semi_major_axis,
#     y0=mean_y - semi_minor_axis,
#     x1=mean_x + semi_major_axis,
#     y1=mean_y + semi_minor_axis,
#     fillcolor="rgba(255, 0, 0, 0.2)",
#     line_color="red",
#     opacity=0.5,
#     name="Эллипс неопределенности",
# )
#
# # Добавление центра эллипса
# fig.add_trace(go.Scatter(
#     x=[mean_x],
#     y=[mean_y],
#     mode="markers",
#     marker=dict(
#         color="blue",
#         size=10
#     ),
#     name="Центр"
# ))
#
# # Настройка осей
# fig.update_layout(
#     xaxis_title="X",
#     yaxis_title="Y",
#     title="Эллипс неопределенности",
#     showlegend=True,
#     autosize=False,
#     width=600,
#     height=400,
# )
#
# # Показ графика
# fig.show()