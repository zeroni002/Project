import numpy as np
from bokeh.plotting import figure, show

x1 = np.arange(0, 10, 1)
y1 = x1**2
y2 = x1**3
y3 = x1**4


p = figure(title="Simple line example", x_axis_label="x", y_axis_label="y")

p.line(x1, y1, legend_label="Quadratic Function", line_width=2, color="red")
p.line(x1, y2, legend_label="Qubic Function", line_width=2, color="green")
p.line(x1, y3, legend_label="QUartic Function", line_width=2, color="blue")

show(p)
