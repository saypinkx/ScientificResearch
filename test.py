from collector import DataManager
from painter import PaintManager
dater = DataManager()
data = dater.load_from_excel('types/j.xlsx')
# data2 = dater.load_from_excel('data/data.xlsx')
cat = PaintManager()
# cat.draw_trajectory_well(data, true_size=1)
cat.draw_trajectory_wells([data], true_size=0).show()
