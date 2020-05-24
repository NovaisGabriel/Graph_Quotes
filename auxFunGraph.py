import numpy as np

def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down=-seed[seed<0].sum()/n

    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100.-100./(1.+rs)

    for i in range(n, len (prices)):
        delta = deltas[i-1]
        if delta >0:
            upval = delta
            downval = 0
        else:
            upval = 0
            downval = -delta
        up = (up*(n-1)+upval)/n
        down = (down*(n-1)+downval)/n
        rs = up/down
        rsi[i] = 100.-100/(1.+rs)
    return rsi

def movingaverage(values, window):
    weights = np.repeat(1.0, window)/window
    smas = np.convolve(values, weights, 'valid')
    return smas

def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values , weights, mode = 'full')[:len(values)]
    a[:window] = a[window]
    return a

def computeMACD(x , slow=26, fast=12):
    '''
    macd line = 12ema-26ema
    signal line = 9ema of the macd line
    histogram = macd line - signal line
    '''
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast - emaslow
