import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use("ggplot")

start = dt.datetime(2000, 1, 1)
end = dt.datetime(2016, 12, 31)

# Fetch data using pandas_datareader
data_frame = web.DataReader("TSLA", "yahoo", start, end)

# Print the first few rows to verify the data retrieval
print(data_frame.head())
