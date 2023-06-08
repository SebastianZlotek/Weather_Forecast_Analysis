from data_manager import DataManager

class Bialystok(DataManager):  
    def __init__(self):
        super().readFile('bialystok')
