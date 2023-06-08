import wx
from bialystok import Bialystok
from bydgoszcz import Bydgoszcz
from chojnice import Chojnice
from elblag import Elblag
from names import names

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Projekt', size=(600, 550))

        # Wczytanie danych miast(tylko raz na początku programu bo chwilę to trwa)
        self.cities = {
            'Białystok': Bialystok(),
            'Bydgoszcz': Bydgoszcz(),
            'Chojnice': Chojnice(),
            'Elbląg': Elblag(),
        } 

        # Interfejs
        panel = wx.Panel(self)                     
        self.cityLst = wx.ListBox(panel, pos=(5, 5), choices=['Białystok', 'Bydgoszcz', 'Chojnice', 'Elbląg'])
        self.intervalLst = wx.ListBox(panel, pos=(120, 5), choices=['Doba', 'Tydzień', 'Miesiąc', 'Rok'])
        wx.StaticText(panel, label="Nr", pos=(210, 25))
        self.nrTextControl = wx.TextCtrl(panel, pos=(230, 20))

        autocorrelation = wx.Button(panel, label='Autokorelacja', pos=(480, 5))
        correlation = wx.Button(panel, label='Korelacja', pos=(480, 30))

        self.name1 = wx.Choice(panel, pos = (350, 5), choices = names)
        self.name2 = wx.Choice(panel, pos = (350, 30), choices = names)

        self.list_ctrl = wx.ListCtrl(panel, pos=(5, 80), size=(575, 420), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Nazwa', width=100)
        self.list_ctrl.InsertColumn(1, 'Średnia', width=100)
        self.list_ctrl.InsertColumn(2, 'Odchylenie standardowe', width=150)
        self.list_ctrl.InsertColumn(3, 'Minimum', width=100)
        self.list_ctrl.InsertColumn(4, 'Maksimum', width=100)

        self.Bind(wx.EVT_LISTBOX, self.onInputChange, self.cityLst)
        self.Bind(wx.EVT_LISTBOX, self.onInputChange, self.intervalLst)
        self.Bind(wx.EVT_TEXT, self.onInputChange, self.nrTextControl)
        self.Bind(wx.EVT_BUTTON, self.onAutocorrelation, autocorrelation)
        self.Bind(wx.EVT_BUTTON, self.onCorrelation, correlation)

        self.Show()

    #Funkcja pomocnicza pobierająca odpowiednie dane do uzupełnienia tabelki
    def getData(self, dataType='average'):
        city = self.cities.get(self.cityLst.GetStringSelection())
        interval = self.intervalLst.GetStringSelection()
        try: 
            nr = int(self.nrTextControl.GetValue())
        except ValueError:
            nr = 1
        if dataType == 'average': return city.getAverage(nr, interval)
        elif dataType == 'std': return city.getStd(nr, interval)
        elif dataType == 'min': return city.getMin(nr, interval)
        elif dataType == 'max': return city.getMax(nr, interval)
        else: return 'no data'

    # Zdarzenie zmiany danych wejściowych, wpisanie danych do tabelki
    def onInputChange(self, event):
        self.list_ctrl.DeleteAllItems()
        k = 0
        for i, v in self.getData('average').items():
            self.list_ctrl.InsertItem(k, i)
            self.list_ctrl.SetItem(k, 1, str(v))
            k += 1
        k = 0
        for v in self.getData('std'):
            self.list_ctrl.SetItem(k, 2, str(v))
            k += 1
        k = 0
        for v in self.getData('min'):
            self.list_ctrl.SetItem(k, 3, str(v))
            k += 1
        k = 0
        for v in self.getData('max'):
            self.list_ctrl.SetItem(k, 4, str(v))
            k += 1

    # Zdarzenie przycisku autokorelacji(trzeba wybrać zakres czasowy i nazwę zmiennej) 
    def onAutocorrelation(self, event):
        city = self.cities.get(self.cityLst.GetStringSelection())
        interval = self.intervalLst.GetStringSelection()
        try: 
            nr = int(self.nrTextControl.GetValue())
        except ValueError:
            nr = 1     
        city.showAutocorrelation(nr, interval=interval, name=self.name1.GetStringSelection())

    # Zdarzenie przycisku korelacji(trzeba wybrać zakres czasowy i 2 zmienne do korelacji) 
    def onCorrelation(self, event):
        city = self.cities.get(self.cityLst.GetStringSelection())
        interval = self.intervalLst.GetStringSelection()
        city.showCorrelation(interval=interval, name1 = self.name1.GetStringSelection(), name2=self.name2.GetStringSelection())
