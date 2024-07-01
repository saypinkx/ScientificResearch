import os


class Deleter:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def delete_excel_data_files(self):
        folder_path = self.base_dir + '/data'
        filenames = os.listdir(folder_path)
        for filename in filenames:
            if filename.endswith(".xlsx"):
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)

    def delete_excel_type_file(self, type: str):
        folder_path = self.base_dir + '/types'
        filenames = os.listdir(folder_path)
        for filename in filenames:
            if filename == f"{type}.xlsx":
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)



deleter = Deleter()
