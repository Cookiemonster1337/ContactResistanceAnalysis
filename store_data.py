import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox


def store_library(file, sample, gdl1, gdl2, spec, ref, thickness):

    # read datafile
    df_input = pd.read_csv(file, sep='\t', decimal=',', encoding='cp1252',
                           error_bad_lines=False)
    # round dataframa values
    df_input.round(2)

    # format dataframe
    # deleting unnecessary columns

    df_input.drop(df_input.columns[[-1, ]], axis=1, inplace=True)

    # rename columns of remaining dataframe
    df_input.rename(columns={df_input.iloc[0,0]:'date', 'Uhrzeit':'time',
                                'Kommentar':'commentary',
                                'p_Probe_Ist / bar':'pressure_sample[bar]',
                                'I_Ist / mA': 'current[mA]',
                                'U_ges / mV':'voltage[mV]',
                                'U_Nadel / mV':'voltage_needle[mV]',
                                'U_ges-Th_U': 'voltage_th[mV]',
                                'U_Nadel-Th_U':'voltage_needle_th[mV]',
                                'Anpressfläche / cm²':'contact_area[cm2]',
                                'p_Ist / bar':'pressure[bar]'},
                                inplace=True)

    # clear measurement artefacts (no current)
    df_input = df_input[df_input['current[mA]'] != 0]

    # fill empty/NaN celss with numerics (0)
    df_input.fillna(0, inplace=True)

    # define commentary / measurement
    commentary_name = 'commentary'
    measurement_name = 'measurement'

    # round pressures and append to df in seperate column
    pressure_rounded = df_input['pressure_sample[bar]'].round(decimals=0)

    # define additional columns for calculations result
    df_input.insert(len(df_input.columns), column='pressure_rounded[bar]',
                    value=pressure_rounded)

    #Probendicke
    sample_thickness = 'sample_thickness[mm]'
    df_input.insert(len(df_input.columns), sample_thickness, 0.0)

    #Gesamtwiderstand
    res_main_col = 'main_resistance[mOhm]'
    df_input.insert(len(df_input.columns), res_main_col, 0.0)

    res_main_mean_col = 'main_resistance_mean[mOhm]'
    df_input.insert(len(df_input.columns), res_main_mean_col, 0.0)

    res_main_error_col = 'main_resistance_error[mOhm]'
    df_input.insert(len(df_input.columns), res_main_error_col, 0.0)

    #Durchgangswiderstand
    res_through_col = 'flow_resistance[mOhm]'
    df_input.insert(len(df_input.columns), res_through_col, 0.0)

    res_through_mean_col = 'flow_resistance_mean[mOhm]'
    df_input.insert(len(df_input.columns), res_through_mean_col, 0.0)

    res_through_error_col = 'flow_resistance_error[mOhm]'
    df_input.insert(len(df_input.columns), res_through_error_col, 0.0)

    #Bulkwiderstand
    res_bulk_col = 'bulk_resistance[mOhm]'
    df_input.insert(len(df_input.columns), res_bulk_col, 0.0)

    res_bulk_mean_col = 'bulk_resistance_mean[mOhm]'
    df_input.insert(len(df_input.columns), res_bulk_mean_col, 0.0)

    res_bulk_error_col = 'bulk_resistance_error[mOhm]'
    df_input.insert(len(df_input.columns), res_bulk_error_col, 0.0)

    res_bulk_sub_col = 'bulk_resistance_sub[mOhm]'
    df_input.insert(len(df_input.columns), res_bulk_sub_col, 0.0)

    #Kontaktwiderstand
    res_contact_col = 'contact_resistance[mOhm]'
    df_input.insert(len(df_input.columns), res_contact_col, 0.0)

    res_contact_mean_col = 'contact_resistance_mean[mOhm]'
    df_input.insert(len(df_input.columns), res_contact_mean_col, 0.0)

    res_contact_error_col = 'contact_resistance_error[mOhm]'
    df_input.insert(len(df_input.columns), res_contact_error_col, 0.0)

    #vs-Gesamtwiderstand
    res_main_vs_col = 'vs_main_resistance[mOhm*cm]'
    df_input.insert(len(df_input.columns), res_main_vs_col, 0.0)

    res_main_vs_mean_col = 'vs_main_resistance_mean[mOhm*cm]'
    df_input.insert(len(df_input.columns), res_main_vs_mean_col, 0.0)

    res_main_vs_error_col = 'vs_main_resistance_error[mOhm*cm]'
    df_input.insert(len(df_input.columns), res_main_vs_error_col, 0.0)

    #vs-Durchgangswiderstand
    res_through_vs_col = 'vs_flow_resistance[mOhm*cm]'
    df_input.insert(len(df_input.columns), res_through_vs_col, 0.0)

    res_through_vs_mean_col = 'vs_flow_resistance_mean[mOhm*cm]'
    df_input.insert(len(df_input.columns), res_through_vs_mean_col, 0.0)

    res_through_vs_error_col = 'vs_flow_resistance_error[mOhm*cm]'
    df_input.insert(len(df_input.columns), res_through_vs_error_col, 0.0)

    #vs-Bulkwiderstand
    res_bulk_vs_col = 'vs_bulk_resistance[mOhm*cm]'
    df_input.insert(len(df_input.columns), res_bulk_vs_col, 0.0)

    res_bulk_vs_mean_col = 'vs_bulk_resistance_mean[mOhm*cm]'
    df_input.insert(len(df_input.columns), res_bulk_vs_mean_col, 0.0)

    res_bulk_vs_error_col = 'vs_bulk_resistance_error[mOhm*cm]'
    df_input.insert(len(df_input.columns), res_bulk_vs_error_col, 0.0)

    #as-Gesamtwiderstand
    res_main_as_col = 'as_main_resistance[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_main_as_col, 0.0)

    res_main_as_mean_col = 'as_main_resistance_mean[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_main_as_mean_col, 0.0)

    res_main_as_error_col = 'as_main_resistance_error[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_main_as_error_col, 0.0)

    #as-Durchgangswiderstand
    res_through_as_col = 'as_through_resistance[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_through_as_col, 0.0)

    res_through_as_mean_col = 'as_through_resistance_mean[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_through_as_mean_col, 0.0)

    res_through_as_error_col = 'as_through_resistance_error[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_through_as_error_col, 0.0)

    #as-Bulkwiderstand
    res_bulk_as_col = 'as_bulk_resistance[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_bulk_as_col, 0.0)

    res_bulk_as_mean_col = 'as_bulk_resistance_mean[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_bulk_as_mean_col, 0.0)

    res_bulk_as_error_col = 'as_bulk_resistance_error[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_bulk_as_error_col, 0.0)

    #as-Kontaktwiderstand
    res_contact_as_col = 'as_contact_resistance[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_contact_as_col, 0.0)

    res_contact_as_mean_col = 'as_contact_resistance_mean[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_contact_as_mean_col, 0.0)

    res_contact_as_error_col = 'as_contact_resistance_error[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_contact_as_error_col, 0.0)

    #vs-Gesamtleitwert
    con_main_vs_col = 'vs_main_conductance[S/cm]'
    df_input.insert(len(df_input.columns), con_main_vs_col, 0.0)

    con_main_vs_mean_col = 'vs_main_conductance_mean[S/cm]'
    df_input.insert(len(df_input.columns), con_main_vs_mean_col, 0.0)

    con_main_vs_error_col = 'vs_main_conductance_error[S/cm]'
    df_input.insert(len(df_input.columns), con_main_vs_error_col, 0.0)

    #vs-Durchgangsleitwert
    con_through_vs_col = 'vs_flow_conductance[S/cm]'
    df_input.insert(len(df_input.columns), con_through_vs_col, 0.0)

    con_through_vs_mean_col = 'vs_flow_conductance_mean[S/cm]'
    df_input.insert(len(df_input.columns), con_through_vs_mean_col, 0.0)

    con_through_vs_error_col = 'vs_flow_conductance_error[S/cm]'
    df_input.insert(len(df_input.columns), con_through_vs_error_col, 0.0)

    #vs-Bulkleitwert
    con_bulk_vs_col = 'vs_flow_conductance[mOhm*cm2]'
    df_input.insert(len(df_input.columns), con_bulk_vs_col, 0.0)

    con_bulk_vs_mean_col = 'vs_flow_conductance_mean[mOhm*cm2]'
    df_input.insert(len(df_input.columns), con_bulk_vs_mean_col, 0.0)

    con_bulk_vs_error_col = 'vs_flow_conductance_error[mOhm*cm2]'
    df_input.insert(len(df_input.columns), con_bulk_vs_error_col, 0.0)

    #spez. GDL-Korrektur
    corr = 'degradation_corr[mOhm*cm2]'
    df_input.insert(len(df_input.columns), corr, 0.0)

    #Messzyklus
    cycle = 'cycle'
    df_input.insert(len(df_input.columns), cycle, 0.0)

    # seperate measurements by cycles
    z = 1
    rec = 0
    for i, v in df_input['pressure_rounded[bar]'].items():
        if v >= rec:

            df_input[cycle].loc[i] = z

            if df_input.loc[v, 'current[mA]'] < 600:
                rec = v
        else:
            z += 1
            rec = 0
            df_input[cycle].iloc[i] = z

    #get unique values as lists --> measurements / pressures / cycles
    measurements = np.unique(df_input[commentary_name].to_numpy())
    pressures = np.unique(pressure_rounded.to_numpy(dtype=int))
    cycles = np.unique(df_input['cycle'].to_numpy(dtype=int))

    #Durchschnittliche Probendicke
    thickness = int(thickness) / 1000
    df_input['sample_thickness[mm]'] = thickness

    #H23 Widerstands und Zyklenkorrektur

    if ref is not 'Referenz' and gdl1 == 'H23':

        df_corr_list = []

        h23_ref = 'h23_reference.csv'
        df_h23 = pd.read_csv(h23_ref)

        for c in cycles:
            df_input_1 = df_input[df_input['cycle'] == c]
            pd.option_context('display.max_columns', None)
            df_h23_1 = df_h23[df_h23['cycle'] == c]

            for p in pressures:
                df_input_2 = df_input_1[df_input_1['pressure_rounded[bar]'] == p]
                df_h23_2 = df_h23_1[df_h23_1['pressure_rounded[bar]'] == p]
                correction_value = df_h23_2[res_main_col].mean()
                df_input_2.loc[df_input_2['pressure_rounded[bar]'] == p, corr] = correction_value
                df_corr_list.append(df_input_2)

        df_input = pd.concat(df_corr_list)

    else:
        df_input.loc[(df_input['pressure_rounded[bar]']) < 31 &
                     (df_input['cycle'] <= 100), corr] = 0

    #TODO: Implementierung SGL 29BC Korrrektur

    # create variable for storage in library --> file_identifier
    file_identifier = ref + ' ' + sample + ' ' + gdl1 + gdl2 + spec

    # create empty df which will be filled with storage data
    df_list = []
    fig, a = plt.subplots(2, 3)

    # seperate datafile into different measurements
    for m in measurements:

        # df-slice with single measurement
        df_t1 = df_input[df_input[commentary_name] == m]

        # specify file-identifer and add measurement
        measurement_identifier = file_identifier + ' ' + m

        # add measurement_identifer / cr / cr_error / cr_mean to df
        df_t1.insert(2, measurement_name, measurement_identifier, True)

        # seperate measurement-df into different cycles
        for c in cycles:

            # df-slice of measurement-df with single 'cycle'
            df_t2_c = df_t1[df_t1[cycle] == c]

            # declare empty y / y-error-value list for plotting --> contact res

            res_main_mean_list = []             #Gesamtwiderstand
            res_main_error_list = []

            res_through_mean_list = []          #Durchgangswiderstand
            res_through_error_list = []

            res_bulk_mean_list = []             #Bulkwiderstand
            res_bulk_error_list = []

            res_contact_mean_list = []          #Kontaktwiderstand
            res_contact_error_list = []

            res_main_vs_mean_list = []          #vs-Gesamtwiderstand
            res_main_vs_error_list = []

            res_through_vs_mean_list = []       #vs-Durchgangswiderstand
            res_through_vs_error_list = []

            res_bulk_vs_mean_list = []          #vs-Bulkwiderstand
            res_bulk_vs_error_list = []

            res_main_as_mean_list = []          #as-Gesamtwiderstand
            res_main_as_error_list = []

            res_through_as_mean_list = []       #as-Durchngangswiderstand
            res_through_as_error_list = []

            res_bulk_as_mean_list = []          #as-Bulkwiderstand
            res_bulk_as_error_list = []

            res_contact_as_mean_list = []       #as-Kontaktwiderstand
            res_contact_as_error_list = []

            con_main_vs_mean_list = []          #vs-Gesamtleitwert
            con_main_vs_error_list = []

            con_through_vs_mean_list = []       #vs-Durchgangsleitwert
            con_through_vs_error_list = []

            con_bulk_vs_mean_list = []          #vs-Bulkleitwert
            con_bulk_vs_error_list = []

            # seperate 'cycle'-df into different pressures

            for p in pressures:

                # df-slice of 'cycle'-df with single pressure

                df_t3 = df_t2_c[df_t2_c['pressure_rounded[bar]'] == p]

                # calculate --> overall resistance

                #Gesamtwiderstand

                res_main = (df_t3['voltage_th[mV]'] / df_t3['current[mA]'])

                #! Korrekturwert s. Korrekturschleife -->[corr]

                #Durchgangswiderstand

                res_through = res_main - df_t3[corr]

                #Bulkwiderstand

                if spec == "m. Nadel":
                    res_bulk = (df_t3['voltage_needle[mV]'] / df_t3['current[mA]'])
                else:
                    res_bulk = (df_t3['voltage_th[mV]'] - df_t3[corr]) / df_t3['current[mA]']

                #Kontaktwiderstand

                res_contact = (res_through - res_bulk) / 2

                #volumenspezifischer Gesamtwiderstand

                res_main_vs = res_main * df_t3['contact_area[cm2]'] / df_t3['sample_thickness[mm]']

                #volumenspezifischer Durchgangswiderstand

                res_through_vs = res_through * df_t3['contact_area[cm2]'] / df_t3['sample_thickness[mm]']

                #volumenspezifischer Bulkwiderstand

                res_bulk_vs = res_bulk * df_t3['contact_area[cm2]'] / df_t3['sample_thickness[mm]']

                # flächenspezifischer Gesamtwiderstand

                res_main_as = res_main *  df_t3['contact_area[cm2]']

                # flächenspezifscher Durchgangswiderstand

                res_through_as = res_through * df_t3['contact_area[cm2]']

                # flächenspezifischer Bulkwiderstand

                res_bulk_as = res_bulk * df_t3['contact_area[cm2]']

                # flächenspezifischer Kontaktwiderstand

                res_contact_as = res_contact * df_t3['contact_area[cm2]']

                # volumenspezifischer Gesamtleitwert

                con_main_vs = 1 / res_main_vs

                # volumenspezifischer Durchgangsleitwert

                con_through_vs = 1 / res_through_vs

                #volumenspezifischer Bulk-Leitwert

                con_bulk_vs = 1 / res_bulk_vs

                # get mean- and sem-value of calculated resistance

                res_main_mean = res_main.mean()
                res_main_error = res_main.sem()

                res_through_mean = res_through.mean()
                res_through_error = res_through.sem()

                res_bulk_mean = res_bulk.mean()
                res_bulk_error = res_bulk.sem()

                res_contact_mean = res_contact.mean()
                res_contact_error = res_contact.sem()

                res_main_vs_mean = res_main_vs.mean()
                res_main_vs_error = res_main_vs.sem()

                res_through_vs_mean = res_through_vs.mean()
                res_through_vs_error = res_through_vs.sem()

                res_bulk_vs_mean = res_bulk_vs.mean()
                res_bulk_vs_error = res_bulk_vs.sem()

                res_main_as_mean = res_main_as.mean()
                res_main_as_error = res_main_as.sem()

                res_through_as_mean = res_through_as.mean()
                res_through_as_error = res_through_as.sem()

                res_bulk_as_mean = res_bulk_as.mean()
                res_bulk_as_error = res_bulk_as.sem()

                res_contact_as_mean = res_contact_as.mean()
                res_contact_as_error = res_contact_as.sem()

                con_main_vs_mean = con_main_vs.mean()
                con_main_vs_error = con_main_vs.sem()

                con_through_vs_mean = con_main_vs.mean()
                con_through_vs_error = con_main_vs.sem()

                con_bulk_vs_mean = con_main_vs.mean()
                con_bulk_vs_error = con_main_vs.sem()

                # write data --> cr-mean and cr-sem in df-slice

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_main_col] = res_main
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_main_mean_col] = res_main_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_main_error_col] = res_main_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_through_col] = res_through
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_through_mean_col] = res_through_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_through_error_col] = res_through_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_bulk_col] = res_bulk
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_bulk_mean_col] = res_bulk_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_bulk_error_col] = res_bulk_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_contact_col] = res_contact
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_contact_mean_col] = res_contact_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_contact_error_col] = res_contact_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_main_vs_col] = res_main_vs
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_main_vs_mean_col] = res_main_vs_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_main_vs_error_col] = res_main_vs_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_through_vs_col] = res_through_vs
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_through_vs_mean_col] = res_through_vs_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_through_vs_error_col] = res_through_vs_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_bulk_as_col] = res_bulk_vs
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_bulk_as_mean_col] = res_bulk_vs_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_bulk_as_error_col] = res_bulk_vs_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_main_as_col] = res_main_as
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_main_as_mean_col] = res_main_as_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_main_as_error_col] = res_main_as_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_through_as_col] = res_through_as
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_through_as_mean_col] = res_through_as_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_through_as_error_col] = res_through_as_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_bulk_as_col] = res_bulk_as
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_bulk_as_mean_col] = res_bulk_as_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_bulk_as_error_col] = res_bulk_as_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_contact_as_col] = res_contact_as
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_contact_as_mean_col] = res_contact_as_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_contact_as_error_col] = res_contact_as_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, con_main_vs_col] = con_main_vs
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, con_main_vs_mean_col] = con_main_vs_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, con_main_vs_error_col] = con_main_vs_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, con_through_vs_col] = con_through_vs
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, con_through_vs_mean_col] = con_through_vs_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, con_through_vs_error_col] = con_through_vs_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, con_bulk_vs_col] = con_bulk_vs
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_bulk_vs_mean_col] = con_bulk_vs_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, res_bulk_vs_error_col] = con_bulk_vs_error

                # append cr-mean and cr-sem values of single pressure to x,y plotdata

                #Gesamtwiderstand
                res_main_mean_list.append(res_main_mean)
                res_main_error_list.append(res_main_error)

                #Durchgangswiderstand
                res_through_mean_list.append(res_through_mean)
                res_through_error_list.append(res_through_error)

                #Bulkwiderstand
                res_bulk_mean_list.append(res_bulk_mean)
                res_bulk_error_list.append(res_bulk_error)

                #Kontaktwiderstand
                res_contact_mean_list.append(res_contact_mean)
                res_contact_error_list.append(res_contact_error)

                #vs-Gesamtwiderstand
                res_main_vs_mean_list.append(res_contact_as_mean)
                res_main_vs_error_list.append(res_contact_as_error)

                #vs-Durchgangswiderstand
                res_through_vs_mean_list.append(res_through_vs_mean)
                res_through_vs_error_list.append(res_through_vs_error)

                #vs-Bulkwiderstand
                res_bulk_mean_list.append(res_bulk_vs_mean)
                res_bulk_error_list.append(res_bulk_vs_error)

                #as-Gesamtwiderstand
                res_main_as_mean_list.append(res_main_as_mean)
                res_main_as_error_list.append(res_main_as_error)

                #as-Durchgangswiderstand
                res_through_as_mean_list.append(res_through_as_mean)
                res_through_as_error_list.append(res_through_as_error)

                #as-Bulkwiderstand
                res_bulk_as_mean_list.append(res_bulk_as_mean)
                res_bulk_as_error_list.append(res_bulk_as_error)

                #as-Kontaktwiderstand
                res_contact_as_mean_list.append(res_contact_as_mean)
                res_contact_as_error_list.append(res_contact_as_error)

                #vs-Gesamtleitwert
                con_main_vs_mean_list.append(con_main_vs_mean)
                con_main_vs_error_list.append(con_main_vs_error)

                #vs-Durchgangsleitwert
                con_through_vs_mean_list.append(con_through_vs_mean)
                con_through_vs_error_list.append(con_through_vs_error)

                #vs-Bulkleitwert
                con_bulk_vs_mean_list.append(con_bulk_vs_mean)
                con_bulk_vs_error_list.append(con_bulk_vs_error)

                df_list.append(df_t3)

            # forming x,y-value-lists into array

            # TODO: implement error-bars in graphs
            res_main_mean = np.asarray(res_main_mean_list)
            res_main_error = np.asarray(res_main_error_list)

            res_through_mean = np.asarray(res_through_mean_list)
            res_through_error = np.asarray(res_through_error_list)

            res_bulk_mean = np.asarray(res_bulk_mean_list)
            res_bulk_error = np.asarray(res_bulk_error_list)

            res_contact_mean = np.asarray(res_contact_mean_list)
            res_contact_error = np.asarray(res_contact_error_list)

            res_main_vs_mean = np.asarray(res_main_vs_mean_list)
            res_main_vs_error = np.asarray(res_main_vs_error_list)

            res_through_vs_mean = np.asarray(res_through_vs_mean_list)
            res_through_vs_error = np.asarray(res_through_vs_error_list)

            res_bulk_vs_mean = np.asarray(res_bulk_vs_mean_list)
            res_bulk_vs_error = np.asarray(res_bulk_vs_error_list)

            res_main_as_mean = np.asarray(res_main_as_mean_list)
            res_main_as_error = np.asarray(res_main_as_error_list)

            res_through_as_mean = np.asarray(res_through_as_mean_list)
            res_through_as_error = np.asarray(res_through_as_error_list)

            res_bulk_as_mean = np.asarray(res_bulk_as_mean_list)
            res_bulk_as_error = np.asarray(res_bulk_as_error_list)

            res_contact_as_mean = np.asarray(res_contact_as_mean_list)
            res_contact_as_error = np.asarray(res_contact_as_error_list)

            con_main_vs_mean = np.asarray(con_main_vs_mean_list)
            con_main_vs_error = np.asarray(con_main_vs_error_list)

            con_through_vs_mean = np.asarray(con_through_vs_mean_list)
            con_through_vs_error = np.asarray(con_through_vs_error_list)

            con_bulk_vs_mean = np.asarray(con_bulk_vs_mean_list)
            con_bulk_vs_error = np.asarray(con_bulk_vs_error_list)


            # graph --> res_mean over p (every 'cycle' seperate)

            # plt.errorbar(pressures, resistance_mean, yerr=resistance_error, elinewidth=None, capsize=2, label=m + str(c))

            a[0][0].plot(pressures, res_main_mean, label=c)
            a[0][0].set_title('Resistance / Pressure')
            a[0][0].set_xlabel('Pressure [bar]')
            a[0][0].set_ylabel('Resistance [mOhm*cm²]')
            a[0][0].set_xlim([0, max(pressures)])
            a[0][0].set_ylim([0, max(res_main_mean)])
            a[0][0].legend(bbox_to_anchor=(-0.55, 1, 0.4, 0), loc='upper left', mode='expand', ncol=3, fontsize='xx-small', title='Cycle')

            a[0][1].plot(pressures, res_through_mean)
            a[0][1].set_title('Volume Resistance / Pressure')
            a[0][1].set_xlabel('Pressure [bar]')
            a[0][1].set_ylabel('Volume Resistance [mOhm*cm²]')
            a[0][1].set_xlim([0, max(pressures)])
            a[0][1].set_ylim([0, max(res_through_mean)])

            a[0][2].plot(pressures, res_contact_mean)
            a[0][2].set_title('Contact Resistance / Pressure')
            a[0][2].set_xlabel('Pressure [bar]')
            a[0][2].set_ylabel('Contact Resistance [mOhm*cm²]')
            a[0][2].set_xlim([0, max(pressures)])
            a[0][2].set_ylim([min(res_contact_mean), max(res_contact_mean)])

        for p in pressures:

            # declare empty y-value list for plotting --> gdl degradation
            ref_res_mean = []
            ref_res_g_mean = []
            ref_bulk_mean = []

            df_t2_p = df_t1[df_t1['pressure_rounded[bar]'] == p]

            for c in cycles:

                df_t3_c = df_t2_p[df_t2_p[cycle] == c]

                # calculate --> overall resistance
                cycle_res_g = (df_t3_c['voltage_th[mV]'] / df_t3_c['current[mA]']) * 1000.0 * df_t2_p['contact_area[cm2]']

                # calculate --> contact resistance

                cycle_res_bulk = (df_t3_c['voltage_needle_th[mV]'] / df_t3_c['current[mA]']) * 1000 * df_t3_c['contact_area[cm2]']

                # cycle_res = (((df_t3_c['U_ges-Th_U'] / df_t3_c['I_Ist / mA']) -
                #               (df_t3_c['U_Nadel-Th_U'] / df_t3_c['I_Ist / mA'])) / 2.0) * 1000 * df_t3_c['Anpressfläche / cm²']
                cycle_res = (cycle_res_g - cycle_res_bulk) / 2.0

                # get mean resistance of 'cycle' for specific pressure
                ref_res = cycle_res.mean()
                ref_res_g = cycle_res_g.mean()
                ref_res_bulk = cycle_res_bulk.mean()

                # append ref_res of 'cycle' to y-value list
                ref_res_mean.append(ref_res)
                ref_res_g_mean.append(ref_res_g)
                ref_bulk_mean.append(ref_res_bulk)

            ref_res_mean = np.asarray(ref_res_mean)
            ref_res_g_mean = np.asarray(ref_res_g_mean)
            ref_bulk_mean = np.asarray(ref_bulk_mean)

            # graph --> res_mean over cylces (one specific pressure)

            a[1][0].plot(cycles, ref_res_g_mean, label=p)
            a[1][0].set_title('Resistance / Cycles')
            a[1][0].set_xlabel('Measurement Cycle')
            a[1][0].set_ylabel('Resistance [mOhm*cm²]')
            a[1][0].set_xlim([1, max(cycles)])
            #a[1][0].set_ylim([0, max(ref_res_g_mean)+10])
            a[1][0].legend(bbox_to_anchor=(-0.55, 1, 0.2, 0), loc='upper left',
                           mode='expand', fontsize='small', title ='p [bar]')

            a[1][1].plot(cycles, ref_bulk_mean)
            a[1][1].set_title('Bulk-Resistance / Cycles')
            a[1][1].set_xlabel('Measurement Cycle')
            a[1][1].set_ylabel('Bulk-Resistance [mOhm*cm²]')
            a[1][1].set_xlim([1, max(cycles)])
            #a[1][1].set_ylim([0, max(ref_bulk_mean)+10])

            a[1][2].plot(cycles, ref_res_mean)
            a[1][2].set_title('Contact Resistance / Cycles')
            a[1][2].set_xlabel('Measurement Cycle')
            a[1][2].set_ylabel('Contact Resistance [mOhm*cm²]')
            a[1][2].set_xlim([1, max(cycles)])
            #a[1][2].set_ylim([min(ref_res_mean)-0.1, max(ref_res_mean)+0.1])



    df_result = pd.concat(df_list)
    df_import = df_result.sort_values(by=['time'])
    df_import2 = df_import.round(2)

    library_name = 'cr_library.csv'

    if os.path.isfile(library_name):
        with open(library_name, newline='') as file:
            if file.read().find(file_identifier) == -1:
                df_import2.to_csv(library_name, mode='a', header=False)
            else:
                tk.messagebox.showinfo(title='Redundanz',
                                       message='Datei bereits im Archiv')
    else:
        df_import2.to_csv(library_name, mode='w', header=True)

    # Formatiere Plot
    table_data = [
      ["Sample", sample],
      ["GDL", gdl1+gdl2],
      ["Method", spec]
    ]

    table = a[0][0].table(cellText=table_data, colWidths=[.2, .5], loc='bottom',
                      bbox=[0.45, 0.75, 0.5, 0.2])



    for (row, col), cell in table.get_celld().items():
        if col == 0:
            cell.set_height(1.3)
            cell._loc = 'left'
            cell.set_text_props(ma='left', color='b', fontweight=50)
        elif col == 1:
            cell.set_height(1.3)
            cell._loc = 'right'
            cell.set_text_props(ma='right')

    plt.show()





