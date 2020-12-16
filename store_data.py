import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox

def store_library(file, sample, gdl1, gdl2, spec, ref, thickness, gdl_age, comment, frame):

    # read datafile
    df_input = pd.read_csv(file, sep='\t', decimal=',', encoding='cp1252',
                           error_bad_lines=False)

    # round dataframa values
    df_input.round(6)

    # format dataframe
    # deleting unnecessary columns

    df_input.drop(df_input.columns[[-1, ]], axis=1, inplace=True)

    # rename columns of remaining dataframe
    df_input.rename(columns={df_input.iloc[0,0]:'date', 'Uhrzeit':'time',
                                'Kommentar':'measurement',
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

    # round pressures and append to df in seperate column
    pressure_ref = [1, 2, 3, 5, 6, 9, 10, 12, 15, 18, 20, 21, 24, 27, 30]
    pressure_rounded = df_input['pressure_sample[bar]'].round(decimals=0)


    #df_input = df_input[df_input['pressure_sample[bar]'] in pressure_ref]
    # current_rounded = df_input['current[mA]'].round(decimals=-2)

    # define additional columns for calculations result
    df_input.insert(len(df_input.columns), column='pressure_rounded[bar]',
                    value=pressure_rounded)

    for i in range(1, 31):
        print(i)
        if (i in pressure_ref) == False:
            df_input = df_input[df_input['pressure_rounded[bar]'] != i]
            print(i)

    print(df_input)
    # df_input.insert(len(df_input.columns), column='current_rounded[mA]',
    #                 value=current_rounded)

    #Probendicke
    sample_thickness = 'sample_thickness[cm]'
    df_input.insert(len(df_input.columns), sample_thickness, 0.0)

    parameters = 'parameters'
    df_input.insert(len(df_input.columns), parameters , 0.0)

    #mv in V
    mV_in_V = '[mV]_in_[V]'
    df_input.insert(len(df_input.columns), mV_in_V, 0.0)

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
    res_through_as_col = 'as_flow_resistance[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_through_as_col, 0.0)

    res_through_as_mean_col = 'as_flow_resistance_mean[mOhm*cm2]'
    df_input.insert(len(df_input.columns), res_through_as_mean_col, 0.0)

    res_through_as_error_col = 'as_flow_resistance_error[mOhm*cm2]'
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
    con_bulk_vs_col = 'vs_bulk_conductance[S/cm]'
    df_input.insert(len(df_input.columns), con_bulk_vs_col, 0.0)

    con_bulk_vs_mean_col = 'vs_bulk_conductance_mean[S/cm]'
    df_input.insert(len(df_input.columns), con_bulk_vs_mean_col, 0.0)

    con_bulk_vs_error_col = 'vs_bulk_conductance_error[S/cm]'
    df_input.insert(len(df_input.columns), con_bulk_vs_error_col, 0.0)

    #spez. GDL-Korrektur
    corr = 'degradation_corr[mOhm]'
    df_input.insert(len(df_input.columns), corr, 0.0)

    #Messzyklus
    cycle = 'cycle'
    df_input.insert(len(df_input.columns), cycle, 0.0)

    # seperate measurements by cycles
    z = int(gdl_age)

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
    measurements = np.unique(df_input['measurement'].to_numpy())
    pressures = np.unique(pressure_rounded.to_numpy(dtype=int))
    cycles = np.unique(df_input['cycle'].to_numpy(dtype=int))
    #currents = np.unique(df_input[current_rounded])

    #Durchschnittliche Probendicke
    df_input['sample_thickness[cm]'] = float(thickness) / 10
    df_input['[mV] in [V]'] = 1000
    df_input[parameters] = gdl1 + gdl2 + '' + spec

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

    elif ref is not 'Referenz' and gdl2 == '29BC':

        df_corr_list = []

        sgl29_ref = 'sgl29bc_reference.csv'
        df_sgl29 = pd.read_csv(sgl29_ref)

        for c in cycles:
            df_input_1 = df_input[df_input['cycle'] == c]
            pd.option_context('display.max_columns', None)
            df_sgl29_1 = df_sgl29[df_sgl29['cycle'] == c]

            for p in pressures:
                df_input_2 = df_input_1[
                    df_input_1['pressure_rounded[bar]'] == p]
                df_sgl29_2 = df_sgl29_1[df_sgl29_1['pressure_rounded[bar]'] == p]
                correction_value = df_sgl29_2[res_main_col].mean()
                df_input_2.loc[df_input_2[
                                   'pressure_rounded[bar]'] == p, corr] = correction_value
                df_corr_list.append(df_input_2)

        df_input = pd.concat(df_corr_list)


    else:
        df_input.loc[(df_input['pressure_rounded[bar]']) < 31 &
                     (df_input['cycle'] <= 100), corr] = 0

    #TODO: Implementierung SGL 29BC Korrrektur

    # create variable for storage in library --> file_identifier
    #file_identifier = ref + ' ' + sample + ' ' + gdl1 + gdl2 + spec
    file_identifier = sample

    # create empty df which will be filled with storage data
    df_list = []
    fig, a = plt.subplots(2, 3)

    # seperate datafile into different measurements
    for m in measurements:

        # df-slice with single measurement
        df_t1 = df_input[df_input['measurement'] == m]

        # specify file-identifer and add measurement
        measurement_identifier = ref + ' ' + file_identifier + ' '+ comment

        # add measurement_identifer / cr / cr_error / cr_mean to df
        df_t1.insert(2, 'measurement', measurement_identifier, True)

        cycles = np.unique(df_t1['cycle'].to_numpy(dtype=int))

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
                print('measurement: ' + str(m), 'cycle: ' + str(c), 'pressure: ' + str(p))
                # df-slice of 'cycle'-df with single pressure

                df_t3_p = df_t2_c[df_t2_c['pressure_rounded[bar]'] == p]
                print(df_t3_p)

                #df_t4_i = df_t3_p[df_t3_p[current_rounded] == i]

                # calculate --> overall resistance

                #Gesamtwiderstand [mOhm]

                res_main = (df_t3_p['voltage_th[mV]'] / df_t3_p['current[mA]']) * 1000 #4W
                print(df_t3_p['voltage_th[mV]'])
                print(df_t3_p['current[mA]'])

                #! Korrekturwert s. Korrekturschleife -->[corr] in [mOhm]

                #Durchgangswiderstand [mOhm]
                print(res_main)
                res_through = res_main - df_t3_p[corr]
                print(df_t3_p[corr])
                print(res_through)
                #Bulkwiderstand [mOhm]

                if spec == "m. Nadel":
                    res_bulk = (df_t3_p['voltage_needle_th[mV]'] / df_t3_p['current[mA]']) * 1000
                else:
                    res_bulk = res_main - res_main
                print(res_bulk)
                #Kontaktwiderstand [mOhm]

                res_contact = (res_through - res_bulk) / 2
                print(res_contact)
                #volumenspezifischer Gesamtwiderstand [mOhm*cm]

                res_main_vs = res_main * df_t3_p['contact_area[cm2]'] / df_t3_p['sample_thickness[cm]']

                #volumenspezifischer Durchgangswiderstand [mOhm*cm]

                res_through_vs = res_through * df_t3_p['contact_area[cm2]'] / df_t3_p['sample_thickness[cm]']

                #volumenspezifischer Bulkwiderstand [mOhm*cm]

                res_bulk_vs = res_bulk * df_t3_p['contact_area[cm2]'] / df_t3_p['sample_thickness[cm]']

                # flächenspezifischer Gesamtwiderstand [mOhm*cm2]

                res_main_as = res_main * df_t3_p['contact_area[cm2]']

                # flächenspezifscher Durchgangswiderstand [mOhm*cm2]

                res_through_as = res_through * df_t3_p['contact_area[cm2]']

                # flächenspezifischer Bulkwiderstand [mOhm*cm2]

                res_bulk_as = res_bulk * df_t3_p['contact_area[cm2]']

                # flächenspezifischer Kontaktwiderstand [mOhm*cm2]

                res_contact_as = res_contact * df_t3_p['contact_area[cm2]']

                # volumenspezifischer Gesamtleitwert [S/cm]

                con_main_vs = df_input['[mV] in [V]'] / res_main_vs

                # volumenspezifischer Durchgangsleitwert [S/cm]

                con_through_vs = df_input['[mV] in [V]'] / res_through_vs

                #volumenspezifischer Bulk-Leitwert [S/cm]

                con_bulk_vs = df_input['[mV] in [V]'] / res_bulk_vs

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

                con_through_vs_mean = con_through_vs.mean()
                con_through_vs_error = con_through_vs.sem()

                con_bulk_vs_mean = con_bulk_vs.mean()
                con_bulk_vs_error = con_bulk_vs.sem()

                # write data --> cr-mean and cr-sem in df-slice

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_main_col] = res_main
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_main_mean_col] = res_main_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_main_error_col] = res_main_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_through_col] = res_through
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_through_mean_col] = res_through_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_through_error_col] = res_through_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_bulk_col] = res_bulk
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_bulk_mean_col] = res_bulk_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_bulk_error_col] = res_bulk_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_contact_col] = res_contact
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_contact_mean_col] = res_contact_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_contact_error_col] = res_contact_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_main_vs_col] = res_main_vs
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_main_vs_mean_col] = res_main_vs_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_main_vs_error_col] = res_main_vs_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_through_vs_col] = res_through_vs
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_through_vs_mean_col] = res_through_vs_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_through_vs_error_col] = res_through_vs_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_bulk_as_col] = res_bulk_vs
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_bulk_as_mean_col] = res_bulk_vs_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_bulk_as_error_col] = res_bulk_vs_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_main_as_col] = res_main_as
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_main_as_mean_col] = res_main_as_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_main_as_error_col] = res_main_as_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_through_as_col] = res_through_as
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_through_as_mean_col] = res_through_as_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_through_as_error_col] = res_through_as_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_bulk_as_col] = res_bulk_as
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_bulk_as_mean_col] = res_bulk_as_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_bulk_as_error_col] = res_bulk_as_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_contact_as_col] = res_contact_as
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_contact_as_mean_col] = res_contact_as_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, res_contact_as_error_col] = res_contact_as_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, con_main_vs_col] = con_main_vs
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, con_main_vs_mean_col] = con_main_vs_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, con_main_vs_error_col] = con_main_vs_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, con_through_vs_col] = con_through_vs
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, con_through_vs_mean_col] = con_through_vs_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, con_through_vs_error_col] = con_through_vs_error

                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, con_bulk_vs_col] = con_bulk_vs
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, con_bulk_vs_mean_col] = con_bulk_vs_mean
                df_t3_p.loc[df_t3_p['pressure_rounded[bar]'] == p, con_bulk_vs_error_col] = con_bulk_vs_error

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

                df_list.append(df_t3_p)

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
            a[0][1].set_ylim([0, max(res_main_mean)])

            a[0][2].plot(pressures, res_contact_mean)
            a[0][2].set_title('Contact Resistance / Pressure')
            a[0][2].set_xlabel('Pressure [bar]')
            a[0][2].set_ylabel('Contact Resistance [mOhm*cm²]')
            a[0][2].set_xlim([0, max(pressures)])
            a[0][2].set_ylim([0, max(res_main_mean)])

        for p in pressures:

            # declare empty y-value list for plotting --> gdl degradation
            ref_res_main_as_mean = []
            ref_res_through_as_mean = []
            ref_res_bulk_as_mean = []
            ref_res_contact_as_mean = []


            df_t2_p = df_t1[df_t1['pressure_rounded[bar]'] == p]

            for c in cycles:

                df_t3_c = df_t2_p[df_t2_p[cycle] == c]

                # calculate --> overall resistance
                cycle_res_main_as = (df_t3_c['voltage_th[mV]'] / df_t3_c['current[mA]']) * 1000.0 * df_t2_p['contact_area[cm2]']

                # calculate --> contact resistance

                cycle_res_through_as = ((df_t3_c['voltage_th[mV]'] / df_t3_c['current[mA]']) * 1000.0 - df_t3_c[corr]) * df_t2_p['contact_area[cm2]']

                if spec == "m. Nadel":
                    cycle_res_bulk_as = (df_t3_c['voltage_needle_th[mV]'] / df_t3_c['current[mA]']) * 1000 * df_t3_c['contact_area[cm2]']
                else:
                    cycle_res_bulk_as = cycle_res_main_as - cycle_res_main_as

                cycle_res_contact_as = (cycle_res_through_as - cycle_res_bulk_as) / 2.0

                # get mean resistance of 'cycle' for specific pressure
                ref_res_main_as = cycle_res_main_as.mean()
                ref_res_bulk_as = cycle_res_bulk_as.mean()
                ref_res_through_as = cycle_res_through_as.mean()
                ref_res_contact_as = cycle_res_contact_as.mean()

                # append ref_res of 'cycle' to y-value list
                ref_res_main_as_mean.append(ref_res_main_as)
                ref_res_through_as_mean.append(ref_res_through_as)
                ref_res_bulk_as_mean.append(ref_res_bulk_as)
                ref_res_contact_as_mean.append(ref_res_contact_as)

            ref_res_main_as_mean = np.asarray(ref_res_main_as_mean)
            ref_res_through_as_mean = np.asarray(ref_res_through_as_mean)
            ref_res_bulk_as_mean = np.asarray(ref_res_bulk_as_mean)
            ref_res_contact_as_mean = np.asarray(ref_res_contact_as_mean)

            if p == 1:
                ymax = max(ref_res_main_as_mean)
            elif p == 2:
                ymax = max(ref_res_main_as_mean)
            elif p==5:
                ymax = max(ref_res_main_as_mean)

            # graph --> res_mean over cylces (one specific pressure)

            a[1][0].plot(cycles, ref_res_main_as_mean, label=p)
            a[1][0].set_title('Main-Resistance / Cycles')
            a[1][0].set_xlabel('Measurement Cycle')
            a[1][0].set_ylabel('Main-Resistance [mOhm*cm²]')
            a[1][0].set_xlim([min(cycles), max(cycles)])
            a[1][0].set_ylim([0, ymax])
            a[1][0].legend(bbox_to_anchor=(-0.55, 1, 0.2, 0), loc='upper left',
                           mode='expand', fontsize='small', title ='p [bar]')

            a[1][1].plot(cycles, ref_res_through_as_mean)
            a[1][1].set_title('Flow-Resistance / Cycles')
            a[1][1].set_xlabel('Measurement Cycle')
            a[1][1].set_ylabel('Flow Resistance [mOhm*cm²]')
            a[1][1].set_xlim([min(cycles), max(cycles)])
            a[1][1].set_ylim([0, ymax])

            a[1][2].plot(cycles, ref_res_contact_as_mean)
            a[1][2].set_title('Contact Resistance / Cycles')
            a[1][2].set_xlabel('Measurement Cycle')
            a[1][2].set_ylabel('Contact-    Resistance [mOhm*cm²]')
            a[1][2].set_xlim([min(cycles), max(cycles)])
            a[1][2].set_ylim([0, ymax])

    df_result = pd.concat(df_list)
    df_import = df_result.sort_values(by=['time'])
    df_import2 = df_import.round(8)

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

    frame.destroy()
    plt.show()






