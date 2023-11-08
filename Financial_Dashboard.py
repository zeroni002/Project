# df = dataframe

import math
import datetime as dt

import numpy as np
import yfinance as yf

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import TextInput, Button, DatePicker, MultiChoice


# Function
def loaddata(ticker1, ticker2, start, end):
    df1 = yf.download(ticker1, start, end)
    df2 = yf.download(ticker2, start, end)
    return df1, df2


def plotData(data, indicators, sync_axis=None):
    df = data
    gain = df.close > df.open
    loss = df.close < df.open
    width = 12 * 60 * 60 * 1000

    if sync_axis is not None:
        p = figure(
            x_axis_type="datetime",
            tools="pan,wheel_zoom,box_zoom,reset,save",
            width=1000,
            x_range=sync_axis,
        )
    else:
        p = figure(
            x_axis_type="datetime",
            tools="pan,wheel_zoom,box_zoom,reset,save",
            width=1000,
        )

    p.xaxis.major_label_orientation = math.pi / 4
    p.grid.grid_line_alpha = 0.25

    p.segment(df.index, df.high, df.index, df.low, color="black")
    p.vbar(
        df.index[gain],
        width,
        df.open[gain],
        df.close[gain],
        fill_color="#00ff00",
        line_color="#00ff00",
    )
    p.vbar(
        df.index[loss],
        width,
        df.open[loss],
        df.close[loss],
        fill_color="#FF0000",
        line_color="#FF0000",
    )
    return p


def on_button_click(ticker1, ticker2, start, end, indicators):
    df1, df2 = loaddata(ticker1, ticker2, start, end)
    p1 = plotData(df1, indicators)
    p2 = plotData(df2, indicators, sync_axis=p1.x_range)
    curdoc().clear()
    curdoc().add_root(layout)
    curdoc().add_root(row(p1, p2))


# UI layout
stock1_text = TextInput(title="Stock 1")
stock2_text = TextInput(title="Stock 2")
date_picker_from = DatePicker(
    title="Start Date",
    value="2020-01-01",
    min_date="2000-01-01",
    max_date=dt.datetime.now().strftime("%Y-%m-%d"),
)
date_picker_to = DatePicker(
    title="Start Date",
    value="2020-02-01",
    min_date="2000-01-01",
    max_date=dt.datetime.now().strftime("%Y-%m-%d"),
)

indicator_Choice = MultiChoice(
    options=[
        "100 Day SMA",
        "30 Day SMA",
        "15 Day SMA",
        "7 Day SMA",
        "1 Day SMA",
        "Linear Regression Line",
    ]
)

load_button = Button(label="Load data", button_type="success")
load_button.on_click(
    lambda: on_button_click(
        stock1_text.value,
        stock2_text.value,
        date_picker_from.value,
        date_picker_to.value,
        indicator_Choice.value,
    )
)

layout = column(
    stock1_text,
    stock2_text,
    date_picker_from,
    date_picker_to,
    indicator_Choice,
    load_button,
)
####
curdoc().clear()
curdoc().add_root(layout)
