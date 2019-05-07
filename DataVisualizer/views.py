from django.shortcuts import render
import pandas as pd
import logging
from django.contrib import messages
import matplotlib.pyplot as plt

from django.http import HttpResponse
from matplotlib import pylab
from pylab import *
import PIL, PIL.Image
from io import BytesIO

# Create your views here.
csv_name = "";
duplicate_csv_name = ""
csv_data = "";
display_data = "";

def upload(request):
        return render(request,'DataVisualizer/index.html')

def viewcsv(request):
    if request.POST:
        global csv_name,duplicate_csv_name,csv_data, display_data
        csv_name = request.FILES["csv_file"]
        if not csv_name.name.endswith('.csv'):
            messages.error(request, 'Please select CSV File!')
            return render(request,'DataVisualizer/index.html')
        csv_data = pd.read_csv(csv_name)
        csv_name.seek(0)
        display_data = pd.read_csv(csv_name, nrows=5)
        df = pd.DataFrame(display_data)

        column_names = list(csv_data.columns.values)

        #logger = logging.getLogger(__name__)
        #logger.error(display_data)
        #messages.success(request, pd.DataFrame.to_string(csv_data))
        #messages.success(request, column_names)

        context = {
            'column_name': df,
        }

        return render(request, 'DataVisualizer/graph.html',context)

def viewgraph(request):
    if request.POST:
        global csv_name, csv_data, display_data
        data = request.POST.copy()
        column_names = list(csv_data.columns.values)
        x_axis = column_names[int(data.get('xaxis'))-1]
        y_axis = column_names[int(data.get('yaxis'))-1]
        unique_column = ""
        if(data.get('unique')):
            unique_column = column_names[int(data.get('unique'))-1]

        # plt.figure(figsize=(5, 5))
        figure(figsize=(6, 6))
        if (unique_column):
            unique_data_columns = pd.unique(csv_data[unique_column])
            for unique_data_column in unique_data_columns:
                ix = getattr(csv_data, unique_column) == unique_data_column
                x, y = csv_data[x_axis][ix], csv_data[y_axis][ix]
                plot(x, y, ".", label=unique_data_column)
                legend()
                #plt.plot(x, y, ".", label=unique_data_column)
        else:
            x, y = csv_data[x_axis], csv_data[y_axis]
            #plt.plot(x, y, ".")
            plot(x, y, ".")
        xlabel(x_axis)
        ylabel(y_axis)
        # plt.xlabel(x_axis)
        # plt.ylabel(y_axis)
        # plt.legend()

        # x=csv_data[x_axis][ix]
        # y=csv_data[y_axis][ix]
        # plot(x,y)
        #
        # xlabel(x_axis)
        # ylabel(y_axis)
        # title(x_axis+' vs '+y_axis)
        # legend()
        #grid(true)
        buffer = BytesIO()
        canvas = pylab.get_current_fig_manager().canvas
        canvas.draw()
        pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
        #pilImage = pilImage.decode("utf-8")
        pilImage.save(buffer, "PNG")

        return HttpResponse(buffer.getvalue(), content_type="image/png")

        #plt.show()
        context={
            'xaxis':xaxis,
            'yaxis':yaxis,
            'unique':unique,
        }
        #return render(request, 'DataVisualizer/showgraph.html',context)