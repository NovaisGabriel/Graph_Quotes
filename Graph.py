import time
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib.animation as animation
import matplotlib
import pylab

from datetime import datetime
from auxFunGraph import *

matplotlib.rcParams.update({'font.size': 9})


def graphData(stock,MA1,MA2):
    fig.clf()
    try:
        stockFile = 'AMZN.txt'
        with open(stockFile) as file:
            content = file.readlines()
            info = {}
            keys = ['closep', 'highp', 'lowp', 'openp', 'volume']
            
            info['date'] = [datetime.strptime(x.split(',')[0], '%Y%m%d') for x in content]
            for index in range(len(keys)):
                info[keys[index]] = [float(x.split(',')[index + 1].replace('\n', '')) for x in content]

        date, closep, highp, lowp, openp, volume = info['date'], info['closep'], info['highp'], info['lowp'], info['openp'], info['volume']
        
        x = 0
        y = len(date)
        candleAr = []

        while x < y:
            appendLine = date[x],openp[x],closep[x],highp[x],lowp[x],volume[x]
            candleAr.append(appendLine)
            x+=1

        Av1 = movingaverage(closep, MA1)
        Av2 = movingaverage(closep, MA2)

        SP = len(date[MA2-1:])

        try:
            #Main=============================================================
            ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4)
            label1=str(MA1)+' SMA'
            label2=str(MA2)+' SMA'
            ax1.plot(date[:SP], Av1[:SP],color='#006666',label=label1, linewidth=1.5)
            ax1.plot(date[:SP], Av2[:SP],color='#003366',label=label2, linewidth=1.5)
            ax1.grid(True, color='w')  
            ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
            ax1.yaxis.label.set_color("#000000")
            ax1.spines['bottom'].set_color("#000000")
            ax1.spines['top'].set_color("#000000")
            ax1.spines['left'].set_color("#000000")
            ax1.spines['right'].set_color("#000000")
            ax1.tick_params(axis='y', colors='#000000')
            ax1.tick_params(axis='x', colors='#000000')
            plt.ylabel('Stock Price and Volume')
            for label in ax1.xaxis.get_ticklabels():
                label.set_rotation(45)
            #Legend===========================================================    
            maLeg = plt.legend(loc=9, ncol=2, prop={'size':7},fancybox=True, borderaxespad=0.)
            maLeg.get_frame().set_alpha(0.4)
            textEd = pylab.gca().get_legend().get_texts()
            pylab.setp(textEd[0:5], color = '#000000')
            #=================================================================
        except:
            print("Main Graphic Failed...")

        try:
            #Top==============================================================
            ax0 = plt.subplot2grid((6,4), (0,0), sharex=ax1, rowspan=1, colspan=4)
            rsi = rsiFunc(closep)
            rsiCol = '#ff9933'
            posCol = '#009933'
            negCol = '#8f2020'
            ax0.plot(date[1:SP], rsi[1:SP], rsiCol, linewidth=1.5)
            ax0.axhline(70,color = negCol)
            ax0.axhline(30,color = posCol)
            ax0.fill_between(date[:SP],rsi[:SP], 70, where=(rsi[:SP]>=70), facecolor=negCol, edgecolor = negCol)
            ax0.fill_between(date[:SP],rsi[:SP], 30, where=(rsi[:SP]<=30), facecolor=posCol, edgecolor = posCol)
            ax0.spines['bottom'].set_color("#000000")
            ax0.spines['top'].set_color("#000000")
            ax0.spines['left'].set_color("#000000")
            ax0.spines['right'].set_color("#000000")
            ax0.tick_params(axis='y', colors='#000000')
            ax0.tick_params(axis='x', colors='#000000')
            ax0.set_yticks([30,70])
            ax0.yaxis.label.set_color("#000000")
            ax0.set_ylim(0,100)
            ax0.text(0.015, 0.95, 'RSI (14)',va='top', color='#000000', transform = ax0.transAxes)
            # ax0.grid(True,color='#000000')
            plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='lower'))
            plt.ylabel('RSI')
            #==============================================================
        except:
            print("Top Graphic Failed...")

        try:
            #Volume========================================================
            volumeMin = 0
            ax1v = ax1.twinx()
            ax1v.fill_between(date[:SP],volumeMin, volume[:SP], facecolor='#999966', alpha=.5)
            ax1v.axes.yaxis.set_ticklabels([])
            ax1v.grid(False)
            ax1v.spines['bottom'].set_color("#000000")
            ax1v.spines['top'].set_color("#000000")
            ax1v.spines['left'].set_color("#000000")
            ax1v.spines['right'].set_color("#000000")
            ax1v.set_ylim(0, 2*volume.max())
            ax1v.tick_params(axis='x', colors='#000000')
            ax1v.tick_params(axis='y', colors='#000000')
            #===============================================================
        except:
            print("Volume Graphic Failed...")


        try:
            #Bottom=========================================================
            ax2 = plt.subplot2grid((6,4),(5,0),sharex=ax1,rowspan=1,colspan=4)
            fillcolor = '#00ffe8'
            nslow = 26
            nfast = 12
            nema = 9
            emaslow, emafast, macd = computeMACD(closep)
            ema9 = ExpMovingAverage(macd, nema)
            ax2.plot(date[:SP], macd[:SP], color = '#4ee6fd', lw=2)
            ax2.plot(date[:SP], ema9[:SP], color = '#e1edf9', lw=1)
            ax2.fill_between(date[-SP:], macd[:SP]-ema9[:SP], 0, alpha = 0.5, facecolor = fillcolor, edgecolor = fillcolor)
            ax2.text(0.015, 0.95, 'MACD 12,26,9',va='top', color='w', transform = ax2.transAxes)
            ax2.spines['bottom'].set_color("#000000")
            ax2.spines['top'].set_color("#000000")
            ax2.spines['left'].set_color("#000000")
            ax2.spines['right'].set_color("#000000")
            ax2.tick_params(axis='x', colors='#000000')
            ax2.tick_params(axis='y', colors='#000000')
            plt.ylabel('MACD',color='#000000')
            plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
            ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper')) 

            for label in ax2.xaxis.get_ticklabels():
                label.set_rotation(45)
            #===============================================================
        except:
            print("Bottom Graphic Failed...")




        #Config=============================================================
        plt.suptitle(stockFile,color='b')

        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)

        plt.subplots_adjust(left=.10, bottom=.20, right=.94, top=.93, wspace=.20, hspace=.07)
        #===================================================================


        

    except:
        print("General Problems....")

fig = plt.figure(facecolor='#f2f2f2')

graphData('AAPL.txt',12,26)
plt.show()

    
