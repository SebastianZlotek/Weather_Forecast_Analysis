from data_manager import DataManager

class Elblag(DataManager):
    
    def __init__(self):
        super().readFile('elblag')
