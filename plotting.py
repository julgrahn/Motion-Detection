from main import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool

p = figure(x_axis_type = 'datetime', height = 100, width = 500, sizing_mode = 'scale_width', title = "Motion Graph")
p.yaxis.minor_tick_line_color = None
p.yaxis.ticker.desired_num_ticks = 1

hover = HoverTool(tooltips = [("Start: ", "@Start"), ("End: ", "@End")])
p.add_tools(hover)

q = p.quad(left = df["Start"], right = df["End"], bottom = 0, top = 1, color = "purple")

output_file("Graph1.html")
show(p)