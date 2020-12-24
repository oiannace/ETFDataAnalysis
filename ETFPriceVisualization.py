import requests
from bs4 import BeautifulSoup
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import datetime as dt
import matplotlib.dates as mdates
#import tkinter
#from tkinter import *

class ETF:
    def __init__(self, ticker, URL):
        self.ticker = ticker
        self.URL = URL
        self.Dates = []
        self.Prices = []
        
    def getcurrentprice(self):
        page = requests.get(self.URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        Current = soup.find('span', attrs={"data-reactid":"32"})
        return Current.text
    def returnssinceOct2017(self):
        return (self.Prices[-1]/self.Prices[1])
    #def holdingsdistributiongraph(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    def sharepricegraph(self, filename, datetype, pricetype, datecol, pricecol, ma):
        self.Dates = np.genfromtxt(filename, skip_header = 1, delimiter = ',', usecols = datecol, dtype = datetype)
        self.Prices = np.genfromtxt(filename, skip_header = 1, delimiter = ',', usecols = pricecol, dtype = pricetype)

        Datesformat = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in self.Dates]
        CompleteTable = np.column_stack((Datesformat, self.Prices))
        
        fig = plt.figure(1)  
        plt.ion()
        
        plt.xlabel('Date')
        plt.ylabel('Price(CAD)')
        plt.title("VEE.TO, VIU.TO, XIC.TO, XUU.TO" +' (2017-2020)')

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 75))
        plt.plot(Datesformat, self.Prices, label = self.ticker)
        
        plt.legend(bbox_to_anchor=(0.9, 0.33), loc='upper left', borderaxespad=0.)
        
        canvas = FigureCanvasTkAgg(fig,master = ma)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row = 0, column = 1)
            
        plt.gcf().autofmt_xdate()
        
# m = tkinter.Tk() 
     
# VEETO = ETF("VEE.TO", 'https://ca.finance.yahoo.com/quote/VEE.TO/history?p=VEE.TO&.tsrc=fin-srch')
# VIUTO = ETF("VIU.TO", "https://ca.finance.yahoo.com/quote/VIU.TO/")
# XICTO = ETF("XIC.TO", "https://ca.finance.yahoo.com/quote/XIC.TO?p=XIC.TO&.tsrc=fin-srch")
# XUUTO = ETF("XUU.T0", "https://ca.finance.yahoo.com/quote/XUU.TO?p=XUU.TO&.tsrc=fin-srch")

# Currentprices = "CURRENT PRICES\n\n" + VEETO.ticker + " " + VEETO.getcurrentprice() +"\n"+ VIUTO.ticker + " " + VIUTO.getcurrentprice()+ "\n" + XICTO.ticker + " " + XICTO.getcurrentprice()+ "\n" + XUUTO.ticker + " " + XUUTO.getcurrentprice()+"\n",datetime.now()
# Currentpricevar = Message(m, text = Currentprices)
# Currentpricevar.config(width = 110)
# Currentpricevar.grid(row = 0, column = 0)

# VEETO.sharepricegraph("VEE.TO.csv", str, float, 0, 4,m)
# VIUTO.sharepricegraph("VIU.TO.csv", str, float, 0, 4,m)
# XICTO.sharepricegraph("XIC.TO.csv", str, float, 0, 4,m)
# XUUTO.sharepricegraph("XUU.TO.csv", str, float, 0, 4,m)

# #print(VEETO.returnssince2017())
# m.mainloop()