from collector import DataManager
from painter import PaintManager
dater = DataManager()
data = dater.load_from_excel('data/tf1.xlsx')
# data2 = dater.load_from_excel('data/data.xlsx')
cat = PaintManager()
# cat.draw_trajectory_well(data, true_size=1)
cat.draw_position_well(data).show()
