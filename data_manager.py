from names import names
from abc import ABC
import pandas as pd
import matplotlib.pyplot as plt

# Klasa abstrakcyjna z której dziedziczą poszcz. miasta
class DataManager(ABC): 
    def readFile(self, fileName):
        # Wczytanie pliku
        self.frame = pd.read_csv('data/' + fileName + '.txt', sep='\s+', header=None, names=names)
        self.months = []
        self.weeks = []
        self.days = []

        # Podział na wektory dobowe, tygodniowe i miesięczne
        weekDay = 0    
        for i in range(1, 13):
            mFrame = self.frame[self.frame['miesiac'] == i]
            self.months.append(mFrame)
            for k in range( 1, int(len(mFrame) / 24) + 1 ):                 
                weekDay += 1
                self.days.append(mFrame[mFrame['dzien'] == k])
                if weekDay == 7:
                    self.weeks.append(pd.concat(self.days[-7:]))
                    weekDay = 0
        if weekDay != 0:
            self.weeks.append(pd.concat(self.days[-weekDay:]))

    # Funkcje obliczeniowe
    def getAverage(self, nr, interval='Doba'):
        if interval == 'Miesiąc':
            return self.months[nr - 1].mean()
        elif interval == 'Tydzień':
            return self.weeks[nr - 1].mean()
        elif interval == 'Doba':
            return self.days[nr - 1].mean()
        elif interval == 'Rok':
            return self.frame.mean()
        else: return 0

    def getStd(self, nr, interval='Doba'):
        if interval == 'Miesiąc':
            return self.months[nr - 1].std()
        elif interval == 'Tydzień':
            return self.weeks[nr - 1].std()
        elif interval == 'Doba':
            return self.days[nr - 1].std()
        elif interval == 'Rok':
            return self.frame.std()
        else: return 0

    def getMin(self, nr, interval='Doba'):
        if interval == 'Miesiąc':
            return self.months[nr - 1].min()
        elif interval == 'Tydzień':
            return self.weeks[nr - 1].min()
        elif interval == 'Doba':
            return self.days[nr - 1].min()
        elif interval == 'Rok':
            return self.frame.min()
        else: return 0

    def getMax(self, nr, interval='Doba'):
        if interval == 'Miesiąc':
            return self.months[nr - 1].max()
        elif interval == 'Tydzień':
            return self.weeks[nr - 1].max()
        elif interval == 'Doba':
            return self.days[nr - 1].max()
        elif interval == 'Rok':
            return self.frame.max()
        else: return 0

    # Funkcje wykresów
    def showAutocorrelation(self, nr = 1, interval='Doba', name = 'temperatura'):
        data = 0
        if interval == 'Miesiąc':
            data = self.months[nr-1][name]
        elif interval == 'Tydzień':
            data = self.weeks[nr-1][name]
        elif interval == 'Doba':
            data = self.days[nr-1][name]
        elif interval == 'Rok':
            data = self.frame[name]
        else: return 0
        x = pd.plotting.autocorrelation_plot(data) 
        x.plot() 
        plt.show()

    def showCorrelation(self, interval='Doba', name1 = 'temperatura', name2 = 'wilgotnosc'):
        data = 0
        if interval == 'Miesiąc':
            data = self.months
        elif interval == 'Tydzień':
            data = self.weeks
        elif interval == 'Doba':
            data = self.days
        elif interval == 'Rok':
            d = self.frame.corr()[name1][name2]
            plt.plot([0,1,2], [d, d, d])
            plt.show()
            return
        else: return 0        
        p = []
        for m in data:
            p.append(m.corr()[name1][name2])
        plt.plot(range(1, len(data)+1), p)
        plt.show()