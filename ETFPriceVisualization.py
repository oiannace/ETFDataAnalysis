import requests
from bs4 import BeautifulSoup
import numpy as np
import sklearn
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import datetime as dt
import matplotlib.dates as mdates
import statistics
#import tkinter
#from tkinter import *

class ETF:
    def __init__(self, ticker, URL):
        
        self.ticker = ticker
        self.URL = URL
        self.Dates = []
        self.Prices = []
        self.OpenPrices = []
        self.tradingvolume = []
        self.sectors = []
    def getcurrentprice(self):
        
        source = requests.get(self.URL).text
        
        soup = BeautifulSoup(source, 'html.parser')

        currentPrice = soup.find('fin-streamer')#, attrs = {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"})

        temp = currentPrice#print(self.ticker, currentPrice.text)
        print(temp)
        return currentPrice['value']
    
    def createDates(self, filename, datetype , datecol):
        tempDates = np.genfromtxt(filename, skip_header = 1, delimiter = ',', usecols = datecol, dtype = datetype)
        self.Dates = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in tempDates]
        
    def annualandmonthlyreturn(self):
        totalreturn = self.Prices[-1]/self.Prices[0]
        
        monthlyreturn = ((totalreturn -1)*100)/60
        Annualreturn = ((totalreturn -1)*100)/5
        return "Annual Return: " + str(round(Annualreturn, 3)) + "%\nMonthly Return: " + str(round(monthlyreturn, 3)) +"%"
    
    def sharepricegraph(self, filename, datetype, pricetype, datecol, pricecol, ma):
        self.createDates(filename,  datetype, datecol)
        self.Prices = np.genfromtxt(filename, skip_header = 1, delimiter = ',', usecols = pricecol, dtype = pricetype)

        CompleteTable = np.column_stack((self.Dates, self.Prices))
        
        fig = plt.figure(1)  
        plt.ion()
        
        plt.xlabel('Date')
        plt.ylabel('Price(CAD)')
        plt.title("VEE.TO, VIU.TO, XIC.TO, XUU.TO" +' (Jan 2016-Jan 2021)')

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 115))
        plt.plot(self.Dates, self.Prices, label = self.ticker)
        
        plt.legend(bbox_to_anchor=(0.9, 0.33), loc='upper left', borderaxespad=0.)
        
        canvas = FigureCanvasTkAgg(fig,master = ma)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row = 0, column = 1)
            
        plt.gcf().autofmt_xdate()
        
    def VolvsOpenPrice(self, filename, datetype, openpricetype, voltype, datecol, openpricecol, volcol, multiplier, ma):
        self.createDates(filename, datetype, datecol)
        self.tradingvolume = np.genfromtxt(filename, skip_header = 1, delimiter = ',', usecols = volcol, dtype = voltype)
        self.OpenPrices = np.genfromtxt(filename, skip_header = 1, delimiter = ',', usecols = openpricecol, dtype = openpricetype)
        for i in range(len(self.tradingvolume)):
            self.tradingvolume[i] = self.tradingvolume[i]*multiplier
        CompleteTable = np.column_stack((self.Dates, self.tradingvolume))
        
        fig = plt.figure(2)  
        plt.ion()
        
        plt.xlabel('Date')
        plt.ylabel('Trading Volume')
        plt.title("Trading Volume (Jan 2016-Jan 2020)")
        
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 115))
        plt.plot(self.Dates, self.tradingvolume, label = self.ticker + "*" + str(multiplier))
        
        plt.legend(bbox_to_anchor=(0.07, 0.9), loc='upper left', borderaxespad=0.)
        
        canvas = FigureCanvasTkAgg(fig,master = ma)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row = 1, column = 1)
        
        plt.gcf().autofmt_xdate()
        
    def holdingspiechart(self,  filename, sectortype, weighttype, sectorcol, weightcol, ma):
        self.sectors = np.genfromtxt(filename, skip_header = 11, delimiter = ',', usecols = sectorcol, dtype = sectortype)
        self.weights = np.genfromtxt(filename, skip_header = 11, delimiter = ',', usecols = weightcol, dtype = weighttype)
        
        holdings = list(set(self.sectors))
        holdingnumbers = []
        holdingweights = []
        
        for i in holdings:
            count = 0
            weight = 0
            for j in range(len(self.sectors)):
                if(i == self.sectors[j]):
                    weight += self.weights[j]
                    count += 1
            holdingnumbers.append(count)
            holdingweights.append(weight)
        
        fig = plt.figure(3)
        plt.pie(holdingnumbers, labels = holdings, autopct = '%1.1f%%')
        plt.axis('equal')
        plt.title("XIC Sector Breakdown by Number of Holdings")
        
        fig2 = plt.figure(4)
        plt.pie(holdingweights, labels = holdings, autopct = '%1.1f%%')
        plt.axis('equal')
        plt.title("XIC Sector Breakdown by Market Value")
       
        canvas = FigureCanvasTkAgg(fig,master = ma)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row = 0, column = 2)
        
        canvas2 = FigureCanvasTkAgg(fig2,master = ma)
        plot_widget = canvas2.get_tk_widget()
        plot_widget.grid(row = 1, column = 2)
    
    def volatility(self, filename, col, dtype, header, ma, num):
        volatility = statistics.stdev(self.Prices)
        numofholdings = len(np.genfromtxt(filename, skip_header = header, delimiter = ',', usecols = col, dtype = dtype))
        fig = plt.figure(5)
        plt.bar(self.ticker, max(self.Prices) - min(self.Prices), width = 0.5, bottom = min(self.Prices))
        plt.ylim(ymin = 0, ymax = 45)
        plt.ylabel('Price Range (CAD)')
        plt.title('Volatility of ETF Closing Price Over 5 Years using Standard Deviation')
        
        plt.annotate("SD = " + str(round(volatility, 4)), xy =( num, 10))
        plt.annotate("Current\nHoldings: \n    " + str(numofholdings), xy = (num, 2))
       
        canvas = FigureCanvasTkAgg(fig, master = ma)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row = 0, column = 3)