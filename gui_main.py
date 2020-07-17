import tkinter as tk
from filedialog import get_file
import pandas as pd
import matplotlib
from matplotlib.figure import Figure
import numpy as np
from tkinter import Frame
from tkinter import PhotoImage
from PIL import ImageTk, Image
import glob

from plot_data import plot_data
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plotter2(dropdown_var, df, canvas, subf):
    df_data = df[df['measurement'] == dropdown_var]
    meas = np.unique(df_data['measurement'].to_numpy())
    df_data.sort_values(by=['pressure_rounded[bar]'], inplace=True)
    df_pressure = df_data['pressure_rounded[bar]']
    pressures = np.unique(df_data['pressure_rounded[bar]'].to_numpy(dtype=int))

    df_res_mean = []
    df_contact_res_mean = []
    df_volume_res_mean = []
    df_bulk_res_mean = []

    for p in pressures:

        df_data2 = df_data[df_data['pressure_rounded[bar]'] == p]
        res_plot = df_data2['resistance_mean[mOhm*cm2]']
        contact_res_plot = df_data2['contact_resistance_mean[mOhm*cm2]']
        volume_res_plot = df_data2['volume_resistance_mean[mOhm*cm2]']
        bulk_res_plot = df_data2['bulk_resistance_mean[mOhm*cm2]']

        res_mean_plot = res_plot.mean()
        contact_res_mean_plot = contact_res_plot.mean()
        volume_res_mean_plot = volume_res_plot.mean()
        bulk_res_mean_plot = bulk_res_plot.mean()

        df_res_mean.append(res_mean_plot)
        df_contact_res_mean.append(contact_res_mean_plot)
        df_volume_res_mean.append(volume_res_mean_plot)
        df_bulk_res_mean.append(bulk_res_mean_plot)


    #df_res_mean = df_data['resistance_mean[mOhm*cm2]']
    df_contact_res = df_data['contact_resistance_mean[mOhm*cm2]']
    df_res = df_data['resistance_mean[mOhm*cm2]']
    #df_y = [rmean for rmean in df_data['Contact Resistance / mOhm*cm²'] ]

    #subf.scatter(df_pressure, df_res, label=dropdown_var)
    #subf.plot(df_pressure, df_res_mean)

    # subf.plot(pressures, df_res_mean, label=meas)
    # subf.plot(pressures, df_contact_res_mean, label='Contact Resistance')
    # subf.plot(pressures, df_volume_res_mean, label='Volume Resistance')
    # subf.plot(pressures, df_bulk_res_mean, label='Bulk Resistance')

    subf.plot(pressures, df_contact_res_mean, label=meas)
    #subf.title('SGL 29BC')
    subf.legend(loc='upper right')
    canvas.draw()

def create_archive():
    archive = tk.Toplevel()
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
                                                      plot_canvas, ax))
    option.pack()

    fig = Figure(figsize=(50, 50))

    font = {'family': 'arial',
            'color': 'black',
            'weight': 'normal',
            'size': 16}

    ax = fig.add_subplot()

    ax.set_xlabel('Contact Pressure / bar', fontdict=font, fontsize=14, labelpad=20)
    ax.set_ylabel('Contact Resistance / mOhm*cm²', fontdict=font, fontsize=14, labelpad=20)
    ax.set_title('Contact Resistance PP-789 <-> PP-791 (H23)', fontdict=font, fontsize=16)
    ax.set_xlim([0, 30])
    ax.set_ylim([0, 250])
    ax.legend(loc="upper right")

    plot_canvas = FigureCanvasTkAgg(fig, master=archive)
    plot_canvas.get_tk_widget().pack()

    archive.mainloop()

menu = tk.Tk()
menu.title("Contact Resistance Analysis")
menu.geometry("{}x{}".format(500, 350))
menu.maxsize(500, 350)
menu.config(bg='lightgrey')

top = Frame(menu, bg='lightgrey', width=500, height=100)
top.grid_propagate(0)
center = Frame(menu, bg='grey', width=500, height=250)
center.grid_propagate(0)

menu.grid_rowconfigure(0, weight=1)
menu.grid_rowconfigure(1, weight=1)

top.grid(row=0)
center.grid(row=1)

#top.grid_rowconfigure(0, weight=1)
#top.grid_rowconfigure(1, weight=1)
#top.grid_columnconfigure(0, minsize=50, weight=1)
#top.grid_columnconfigure(1, minsize=50, weight=1)

button1 = tk.Button(top, text='Import new Measurement', width=40,
                    command=get_file)

button2 = tk.Button(top, text='Open Archive', width=40,
                    command=lambda:create_archive())

im_cr = Image.open('cr_test.png')
im_zbt = Image.open('zbt.png')

ph_cr = ImageTk.PhotoImage(im_cr.resize((200, 200), Image.ANTIALIAS))
ph_zbt = ImageTk.PhotoImage(im_zbt.resize((100, 50), Image.ANTIALIAS))

label_ph_cr = tk.Label(center, image=ph_cr, width=200, height=200)
label_ph_zbt = tk.Label(top, image=ph_zbt, width=100, height=50)

button1.grid(padx=(20, 0), pady=10, row=0, column=0, sticky='w')
button2.grid(padx=(20, 0), pady=10, row=1, column=0, sticky='w')

label_ph_cr.grid(padx=150, pady=10)
label_ph_zbt.grid(padx=80, row=0, column=1, sticky='ne')

menu.mainloop()

#plot data for archive canvas

