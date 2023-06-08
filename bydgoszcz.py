from data_manager import DataManager

class Bydgoszcz(DataManager):
    
    def __init__(self):
        super().readFile('bydgoszcz')
