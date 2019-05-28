import plotly as py
from plotly import tools
import plotly.graph_objs as go
from TA.GetHA import *
from DataManagement.ConvertToPandas import *
from TA.GetSLOPE import *


def PlotQuick(prices, dates):

    # converting the input to Pandas and Creating the Heiken Ashi sequence
    df = ConvertToPandas(prices, dates)
    ha = GetHA(prices)
    ha = ConvertToPandas(ha, dates)

    # creating the Technical Indicators
    ma = df.close.rolling(center=False, window=30).mean()
    a = GetSLOPE(prices, [25])
    a = ConvertToPandas(a[25], dates)
    # c = ConvertToPandas(a['signal'], dates)
    # d = ConvertToPandas(a['diff'], dates)

    # creating the graph windows
    trace0 = go.Ohlc(x=df.index, open=df.open, high=df.high, low=df.low, close=df.close, name='Currency')
    trace1 = go.Scatter(x=df.index, y=ma, name='MA30')
    # trace2 = go.Bar(x=df.index, y=df.volume)
    # trace2 = go.Ohlc(x=df2.index, open=df2.open, high=df2.high, low=df2.low, close=df2.close, name='HeikenAshi')
    trace2 = go.Scatter(x=a.index, y=a.TI, name='12')
    # trace3 = go.Scatter(x=c.index, y=c.TI, name='12')
    # trace4 = go.Bar(x=d.index, y=d.TI, name='12')


    # Plotting the graphs
    fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)
    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 2, 1)
    # fig.append_trace(trace3, 2, 1)
    # fig.append_trace(trace4, 2, 1)



    py.offline.plot(fig, filename='temp.html')
