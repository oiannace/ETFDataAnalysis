# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 13:00:25 2020

@author: Ornello
"""
import tkinter
from tkinter import *
from datetime import datetime
import datetime as dt
import ETFPriceVisualization
m = tkinter.Tk() 
     
VEETO = ETFPriceVisualization.ETF("VEE.TO", 'https://ca.finance.yahoo.com/quote/VEE.TO/history?p=VEE.TO&.tsrc=fin-srch')
VIUTO = ETFPriceVisualization.ETF("VIU.TO", "https://ca.finance.yahoo.com/quote/VIU.TO/")
XICTO = ETFPriceVisualization.ETF("XIC.TO", "https://ca.finance.yahoo.com/quote/XIC.TO?p=XIC.TO&.tsrc=fin-srch")
XUUTO = ETFPriceVisualization.ETF("XUU.T0", "https://ca.finance.yahoo.com/quote/XUU.TO?p=XUU.TO&.tsrc=fin-srch")


VEETO.sharepricegraph("VEE.TO.csv", str, float, 0, 4,m)
VIUTO.sharepricegraph("VIU.TO.csv", str, float, 0, 4,m)
XICTO.sharepricegraph("XIC.TO.csv", str, float, 0, 4,m)
XUUTO.sharepricegraph("XUU.TO.csv", str, float, 0, 4,m)

VEETO.VolvsOpenPrice("VEE.TO.csv", str, float, int, 0, 1, 6, 10, m)
VIUTO.VolvsOpenPrice("VIU.TO.csv", str, float, int, 0, 1, 6, 10, m)
XICTO.VolvsOpenPrice("XIC.TO.csv", str, float, int, 0, 1, 6, 1, m)
XUUTO.VolvsOpenPrice("XUU.TO.csv", str, float, int, 0, 1, 6, 10, m)
Overview = "CURRENT PRICES\n\n" + VEETO.ticker + " " + VEETO.getcurrentprice() +"\n" + VIUTO.ticker + " " + VIUTO.getcurrentprice()+ "\n" + XICTO.ticker + " " + XICTO.getcurrentprice()+ "\n" + XUUTO.ticker + " " + XUUTO.getcurrentprice()+"\n",datetime.now()
Currentpricevar = Message(m, text = Overview)
Currentpricevar.config(width = 110)
Currentpricevar.grid(row = 0, column = 0)
#print(VEETO.returnssince2017())
m.mainloop()
