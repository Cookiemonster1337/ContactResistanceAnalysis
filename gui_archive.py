import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib

from plot_data import plot_data
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#plot data for archive canvas
def plotter2(dropdown_var, df, canvas):
    df_data = df[df['measurement'] == dropdown_var]
    df_data.sort_values(by=['pressure_rounded[bar]'], inplace=True)
    df_x = df_data['pressure_rounded[bar]']
    df_y_mean = df_data['resistance_mean[mOhm*cm2]']
    df_y_scatter = df_data['resistance[mOhm*cm2]']
    #df_y = [rmean for rmean in df_data['Contact Resistance / mOhm*cm²'] ]

    ax.scatter(df_x, df_y_scatter, label=dropdown_var)
    ax.plot(df_x, df_y_mean)
    canvas.draw()

archive = tk.Tk()
archive.title('Archive')
archive.geometry('1000x1000')
archive.grid_columnconfigure((0, 0), weight=1)

#read library and get names of measurements
df_lib = pd.read_csv('cr_library.csv', sep='\t')
measurement_name = df_lib['measurement'].unique()

#set startvalue and define optionmenu
var = tk.StringVar(archive)
var.set(measurement_name[0])
option = tk.OptionMenu(archive, var, *measurement_name,
                       command=lambda _: plotter2(var.get(), df_lib,
                                                  plot_canvas))
option.pack()

fig = Figure(figsize=(50, 50))
ax = fig.add_subplot()

ax.set_xlabel('Contact Pressure / bar')
ax.set_ylabel('Contact Resistance / mOhm*cm²')
ax.set_title('Contact Resistance', fontsize=16)
ax.legend(loc="upper right")

plot_canvas = FigureCanvasTkAgg(fig, master=archive)
plot_canvas.get_tk_widget().pack()

# def plotter(x, frame):
#     fig = Figure(figsize=(50, 50))
#     ax = fig.add_subplot(111)
#     ax.scatter(plot_data(x)[0], plot_data(x)[1], color='red')
#     #a.plot(plotData(x)[0], plotData(x)[1], color='blue')
#     #a.scatter(plotData(var.get())[0], plotData(var.get())[1], color='red')
#     # a.plot(plotData(var.get())[0], plotData(var.get())[1], color='blue')
#
#     ax.set_xlabel('Contact Pressure / bar')
#     ax.set_ylabel('Contact Resistance / mOhm*cm²')
#     ax.set_title('Contact Resistance', fontsize = 16)
#
#     #graph = plt.errorbar(pressures, resistance_mean, yerr=resistance_error, elinewidth=None, capsize=2, label=meas)
#
#     canvas = FigureCanvasTkAgg(fig, master=frame)
#     #canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
#     canvas.draw()
#     fig.canvas.draw_idle()








    # fig.canvas.draw_idle()




    # initial value

# x = np.linspace(0, 10, 10)
# y = np.random.rand(10)
# fig = Figure(figsize=(50, 50))
# ax = fig.add_subplot(111)
# ax.scatter(x, y, color='red')
# a.plot(plotData(x)[0], plotData(x)[1], color='blue')
# a.scatter(plotData(var.get())[0], plotData(var.get())[1], color='red')
# a.plot(plotData(var.get())[0], plotData(var.get())[1], color='blue')

# ax.set_xlabel('Contact Pressure / bar')
# ax.set_ylabel('Contact Resistance / mOhm*cm²')
# ax.set_title('Contact Resistance', fontsize=16)

# graph = plt.errorbar(pressures, resistance_mean, yerr=resistance_error, elinewidth=None, capsize=2, label=meas)

# canvas = FigureCanvasTkAgg(fig, master=archive)
# canvas.draw()
# canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
# canvas.draw()
# fig.canvas.draw_idle()



# fig = Figure(figsize=(200, 200))
# a = fig.add_subplot(111)
# a.scatter(plotData(var.get())[0],plotData(var.get())[1], color='red')
# a.plot(plotData(var.get())[0],plotData(var.get())[1], color='blue')
# plt.plot
#
# a.set_xlabel('Contact Pressure / bar')
# a.set_ylabel('Contact Resistance / mOhm*cm²')
# a.set_title('Contact Resistance', fontsize = 16)
#
# graph = plt.errorbar(pressures, resistance_mean, yerr=resistance_error, elinewidth=None, capsize=2, label=meas)
#
# canvas = FigureCanvasTkAgg(fig, master=archive)
# canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
# canvas.draw()

# plt.legend()
# plt.show()

archive.mainloop()
