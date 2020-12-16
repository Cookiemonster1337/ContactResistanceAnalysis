import tkinter as tk
import pandas as pd
import matplotlib.gridspec
from matplotlib.figure import Figure
import numpy as np
import tkinter.filedialog
from gui_doc import import_data
from tkinter import Frame
from PIL import ImageTk, Image

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_file(frame):
    filename = \
        tk.filedialog.askopenfilename(initialdir="C:/Users/Julian/Desktop/neu/Präsentation/Kontaktwiderstände",
                                      title="Select file",
                                      filetypes=(
                                                 ("all files", "*.*"),
                                                 ("Text files", "*.txt")))
    import_data(frame, filename)


def plotter2(dropdown_var, df, canvas, subf1, subf2,subf3, subf4, subf5):

    df_data = df[df['measurement'] == dropdown_var]
    meas = np.unique(df_data['measurement'].to_numpy())
    x = str(meas).split()
    bar_name = x[1]
    df_data.sort_values(by=['pressure_rounded[bar]'], inplace=True)
    pressures = np.unique(df_data['pressure_rounded[bar]'].to_numpy(dtype=int))

    df_res_main_as_mean = []
    df_res_flow_as_mean = []
    df_res_bulk_as_mean = []
    df_res_contact_as_mean = []

    df_con_main_vs_mean = []
    df_con_flow_vs_mean = []
    df_con_bulk_vs_mean = []

    for p in pressures:

        df_data2 = df_data[df_data['pressure_rounded[bar]'] == p]

        res_main_as_plot = df_data2['as_main_resistance_mean[mOhm*cm2]']
        res_through_as_plot = df_data2['as_flow_resistance_mean[mOhm*cm2]']
        res_bulk_as_plot = df_data2['as_bulk_resistance_mean[mOhm*cm2]']
        res_contact_as_plot = df_data2['as_contact_resistance_mean[mOhm*cm2]']

        res_main_vs_plot = df_data2['vs_main_resistance_mean[mOhm*cm]']
        res_through_vs_plot = df_data2['vs_flow_resistance_mean[mOhm*cm]']
        res_bulk_vs_plot = df_data2['vs_bulk_resistance_mean[mOhm*cm]']

        con_main_vs_plot = df_data2['vs_main_conductance_mean[S/cm]']
        con_through_vs_plot = df_data2['vs_flow_conductance_mean[S/cm]']
        con_bulk_vs_plot = df_data2['vs_bulk_conductance_mean[S/cm]']

        #flächenspezifische Widerstände
        res_main_as_mean_plot = res_main_as_plot.mean()
        res_through_as_mean_plot = res_through_as_plot.mean()
        res_bulk_as_mean_plot = res_bulk_as_plot.mean()
        res_contact_as_mean_plot = res_contact_as_plot.mean()

        #volumenspezifische Widerstände
        res_main_vs_mean_plot = res_main_vs_plot.mean()
        res_through_vs_mean_plot = res_through_vs_plot.mean()
        res_bulk_vs_mean_plot = res_bulk_vs_plot.mean()

        #Leitwerte
        con_main_vs_mean_plot = con_main_vs_plot.mean()
        con_through_vs_mean_plot = con_through_vs_plot.mean()
        con_bulk_vs_mean_plot = con_bulk_vs_plot.mean()

        if p == 10:
            mr_as_at_10bar = res_main_as_mean_plot
            fr_as_at_10bar = res_through_as_mean_plot
            br_as_at_10bar = res_bulk_as_mean_plot
            cr_as_at_10bar = res_contact_as_mean_plot

            mr_vs_at_10bar = res_main_vs_mean_plot
            fr_vs_at_10bar = res_through_vs_mean_plot
            br_vs_at_10bar = res_bulk_vs_mean_plot

            con_mvs_at_10bar = con_main_vs_mean_plot
            con_fvs_at_10bar = con_through_vs_mean_plot
            con_bvs_at_10bar = con_bulk_vs_mean_plot

        if p == 20:
            mr_as_at_20bar = res_main_as_mean_plot
            fr_as_at_20bar = res_through_as_mean_plot
            br_as_at_20bar = res_bulk_as_mean_plot
            cr_as_at_20bar = res_contact_as_mean_plot

            mr_vs_at_20bar = res_main_vs_mean_plot
            fr_vs_at_20bar = res_through_vs_mean_plot
            br_vs_at_20bar = res_bulk_vs_mean_plot

            con_mvs_at_20bar = con_main_vs_mean_plot
            con_fvs_at_20bar = con_through_vs_mean_plot
            con_bvs_at_20bar = con_bulk_vs_mean_plot

        df_res_main_as_mean.append(res_main_as_mean_plot)
        df_res_flow_as_mean.append(res_through_as_mean_plot)
        df_res_bulk_as_mean.append(res_bulk_as_mean_plot)
        df_res_contact_as_mean.append(res_contact_as_mean_plot)

    # table_data = [
    #     ["GDL", ''],
    #     ["Method", '']
    #     ['Specific', '']
    # ]


    subf1.plot(pressures, df_res_contact_as_mean, linestyle='dashed', linewidth=2, marker='s', markersize=4, label=meas)
    subf1.legend(loc='upper left', bbox_to_anchor=(-0.28, 1.15), ncol=8, fontsize=8)
    subf1.set_xlabel('Anpressdruck [bar]', labelpad=10, fontdict=dict(fontsize=12, weight='bold'))
    subf1.set_ylabel('Durchgangswiderstand [mOhm*cm2]', labelpad=10, fontdict=dict(fontsize=12, weight='bold'))
    #subf1.table(cellText=table_data, colWidths=[.2, .5], loc='bottom', bbox=[0, -0.4, 0.6, 0.25])

    subf2.bar(bar_name, fr_as_at_10bar, width=1)
    subf2.tick_params('x', labelsize=8, labelrotation=35)
    subf2.set_ylabel('[mOhm*cm2]', labelpad=10)

    subf3.bar(bar_name, con_mvs_at_10bar, width=1)
    subf3.tick_params('x', labelsize=8, labelrotation=35)
    subf3.set_ylabel('[S/cm]', labelpad=10)

    subf4.bar(bar_name, con_fvs_at_10bar, width=1)
    subf4.tick_params('x', labelsize=8, labelrotation=35)
    subf4.set_ylabel('[S/cm]', labelpad=10)

    subf5.bar(bar_name, con_bvs_at_10bar, width=1)
    subf5.tick_params('x', labelsize=8, labelrotation=35)
    subf5.set_ylabel('[S/cm]', labelpad=10)



    # subf6.table(cellText=table_data, colWidths=[.2, .5], loc='bottom',
    #                   bbox=[0.45, 0.75, 0.5, 0.2])


    canvas.draw()

def create_archive():
    archive = tk.Toplevel(menu)
    archive.title('Archive')
    archive.geometry('2000x1000')
    archive.iconbitmap('zbt_logo.ico')

    # top = Frame(archive, bg='lightgrey', width=600, height=275)
    # top.grid_propagate(0)
    # bot = Frame(archive, bg='grey', width=600, height=25)
    # bot.grid_propagate(0)

    #top.grid_columnconfigure((0, 0), weight=1)
    # bot.grid_columnconfigure((0, 0), weight=1)


    # #read library and get names of measurements
    df_lib = pd.read_csv('cr_library.csv', delimiter=',')
    measurement_name = df_lib['measurement'].unique()

    #set startvalue and define optionmenu
    var = tk.StringVar(archive)
    var.set(measurement_name[0])
    option = tk.OptionMenu(archive, var, *measurement_name,
                           command=lambda _: plotter2(var.get(), df_lib,
                                                      plot_canvas, fig_ax1, fig_ax2, fig_ax3, fig_ax4, fig_ax5))

    option.pack()

    varmr = '1'
    checkbutton1 = tk.Checkbutton(archive, text="Gesamtwiderstand",
                                  variable=varmr,
                                  onvalue="GW", offvalue="",
                                  bg='lightgrey')
    varfr = '2'
    checkbutton2 = tk.Checkbutton(archive, text="Durchgangswiderstand",
                                  variable=varfr,
                                  onvalue="DW", offvalue="",
                                  bg='lightgrey')
    varcr = '3'
    checkbutton3 = tk.Checkbutton(archive, text="Kontaktwiderstand",
                                  variable=varcr,
                                  onvalue="KW", offvalue="",
                                  bg='lightgrey')
    # checkbutton1.pack()
    # checkbutton2.pack()
    # checkbutton3.pack()

    fig = Figure(figsize=(50, 50))
    grid = fig.add_gridspec(13, 18)

    fig_ax1 = fig.add_subplot(grid[:13, :-8])
    fig_ax1.set_title('Durchgangswiderstand', pad=10, fontdict=dict(fontsize=16, weight='bold'))
    # fig_ax1.text(0.05, -0.1, table_data, style='italic',
    #     bbox={'facecolor': 'blue', 'alpha': 0.5, 'pad': 10})

    #fig_ax1.table('test', cellColours='blue', bbox=[0.05, -0.1, 0.5, 0.2])
    fig_ax1.set_xlim([0, 20])
    fig_ax1.set_ylim([0, 400])

    fig_ax2 = fig.add_subplot(grid[1:6, 5:9])
    fig_ax2.set_title('Durchgangswiderstand @ 10bar', fontdict=dict(fontsize=10, weight='bold'))

    fig_ax3 = fig.add_subplot(grid[0:3, 12:])
    fig_ax3.set_title('volumetrischer Gesamt-Leitwert [S/cm] @ 10bar', pad=10, fontdict=dict(fontsize=10, weight='bold'))

    fig_ax4 = fig.add_subplot(grid[5:8, 12:])
    fig_ax4.set_title('volumetrischer Durchgangs-Leitwert [S/cm] @ 10bar', pad=10, fontdict=dict(fontsize=10, weight='bold'))

    fig_ax5 = fig.add_subplot(grid[10:13, 12:])
    fig_ax5.set_title('volumetrischer Bulk-Leitwert [S/cm] @ 10bar', pad=10, fontdict=dict(fontsize=10, weight='bold'))

    # fig_ax6 = fig.add_subplot(grid[11:13, :-8])
    plot_canvas = FigureCanvasTkAgg(fig, master=archive)
    plot_canvas.get_tk_widget().pack()

    archive.mainloop()

# GUI / Mainwindow

#Init / Mainwindow - Mainframe
menu = tk.Tk()
menu.title("Analyse Kontaktwiderstand")
menu.geometry("{}x{}".format(500, 350))
menu.maxsize(500, 350)
menu.config(bg='lightgrey')
menu.iconbitmap('zbt_logo.ico')

#Init / Mainwindow - Subframes
top = Frame(menu, bg='lightgrey', width=500, height=100)
top.grid_propagate(0)

center = Frame(menu, bg='grey', width=500, height=250)
center.grid_propagate(0)

menu.grid_rowconfigure(0, weight=1)
menu.grid_rowconfigure(1, weight=1)
top.grid(row=0)
center.grid(row=1)

center.grid_columnconfigure(0, minsize=100, weight=1)
center.grid_columnconfigure(1, minsize=100, weight=1)

#Tkinter Objects
button1 = tk.Button(top, text='Import new Measurement', width=40,
                    command=lambda: get_file(menu))

button2 = tk.Button(top, text='Analyze Data', width=40,
                    command=lambda: create_archive())

button1.grid(padx=(20, 0), pady=10, row=0, column=0, sticky='w')
button2.grid(padx=(20, 0), pady=10, row=1, column=0, sticky='w')

#Design (PNG-Import)
im_cr = Image.open('cr_test.png')
im_zbt = Image.open('zbt.png')
im_cr_calc = Image.open('cr_calc.png')

ph_cr = ImageTk.PhotoImage(im_cr.resize((200, 200), Image.ANTIALIAS))
ph_cr_calc = ImageTk.PhotoImage(im_cr_calc.resize((200, 200), Image.ANTIALIAS))
ph_zbt = ImageTk.PhotoImage(im_zbt.resize((100, 50), Image.ANTIALIAS))

label_ph_cr = tk.Label(center, image=ph_cr, width=200, height=200)
label_ph_cr_calc = tk.Label(center, image=ph_cr_calc, width=200, height=200)
label_ph_zbt = tk.Label(top, image=ph_zbt, width=100, height=50)

label_ph_cr.grid(row=0, column=0, pady=20)
label_ph_cr_calc.grid(row=0, column=1, pady=20)
label_ph_zbt.grid(padx=85, row=0, column=1, sticky='ne')

menu.mainloop()

