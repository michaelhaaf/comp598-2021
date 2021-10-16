from random import random

from bokeh.io import show
from bokeh.models import CustomJS, Select, ColumnDataSource, Div

from bokeh.layouts import column
from bokeh.palettes import RdYlBu3, Spectral11
from bokeh.plotting import figure, curdoc, output_file, show

import numpy as np
import calendar
import pickle

### load preprocessed data:
# 1) list of unique zips
# 2) for each zip, the average open -> close time per month

# 1)
def unique_zips():
    with open('./data/unique_zips.pk1', 'rb') as f:
        return pickle.load(f)

# 2)
def avg_close_time(zipcode = None):
    datafile = ""
    if zipcode is None:
        datafile = "average"
    else:
        datafile = zipcode
    with open(f'./data/zips/{datafile}.pk1', 'rb') as f:
        return pickle.load(f)
    

months = calendar.month_abbr[1:]

# create a plot and style its properties
# also create a header
div = Div(text="The Zipcode1 and Zipcode2 data defaults to 0. Select a zipcode to see results!", width=200, height=100)

curdoc().theme= 'night_sky'

p = figure(title='Average incident close time (2020)',
        x_axis_label='Month', y_axis_label='Avg Incident Close Time (hours)',
        x_range=months
        )

r0 = p.line(months, avg_close_time(), color=Spectral11[0], legend_label='All Zipcodes (average)')
r1 = p.line(months, [0]*12, color=Spectral11[5], legend_label='Zipcode 1')
r2 = p.line(months, [0]*12, color=Spectral11[10], legend_label='Zipcode 2')

ds1 = r1.data_source
ds2 = r2.data_source

def callback1(attr, old, new):
    print(f'changed zip code 1 to {new}. used to be {old}')
    ds1.data={'x':months, 'y':avg_close_time(new)}

def callback2(attr, old, new):
    print(f'changed zip code 2 to {new}. used to be {old}')
    ds2.data={'x':months, 'y':avg_close_time(new)}

# add a dropdown widget and configure with the call back
menu = unique_zips()

select1 = Select(title="Zipcode 1", options=menu)
select1.on_change('value', callback1)

select2 = Select(title="Zipcode 2", options=menu)
select2.on_change('value', callback2)

# put the button and plot in a layout and add to the document
# but also handle authentication (bit of a hack)
args = curdoc().session_context.request.arguments
args = {k: v[0].decode("utf-8") for k, v in args.items()}
if args['username'] == 'nyc' and args['password'] == 'iheartnyc':
    curdoc().add_root(column(div, select1, select2, p))
