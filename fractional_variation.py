#!/usr/bin/env python
# coding: utf-8

# Plotting lightcurve and spectrum

#Import relevant functions
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import glob
import pandas as pd
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord, match_coordinates_sky
import argparse
import os
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from collections import defaultdict
import pandas as pd
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec


parser = argparse.ArgumentParser(
        description='Produces a lightcurve for the variable source')

parser.add_argument('on_ref', help="The path where the csv file is for the on data for the variable source")
parser.add_argument('off_ref', help="The path where the csv file is for the off data for the refernce source")

parser.add_argument('--source_name', help="Adding the name of the source to the plots")
parser.add_argument('--fractional_variation', help="Adding the file name to save the plot")
args = parser.parse_args()

on_ref = pd.read_csv(args.on_ref)
off_ref = pd.read_csv(args.off_ref)


# Normalise the reference source and then multiple by 1.5 to seperate from the refernce source

# Calculate the mean flux value
mean_flux_ref_on = on_ref['flux_ref'].mean()
mean_flux_ref_off = off_ref['flux_ref'].mean()

#mean_flux_ref_err_off = off_ref['flux_err_ref'].mean()
#mean_flux_ref_err_on = on_ref['flux_err_ref'].mean()

# Normalize the flux and error by the mean flux value
on_ref['flux_ref_norm'] = (on_ref['flux_ref']/ mean_flux_ref_on)
#on_ref['flux_err_ref_norm'] = (on_ref['flux_err_ref']-mean_flux_ref_err_on / mean_flux_ref_err_on)

off_ref['flux_ref_norm'] = (off_ref['flux_ref']/ mean_flux_ref_off)
#off_ref['flux_err_ref_norm'] = off_ref['flux_err_ref']-mean_flux_ref_err_off / mean_flux_ref_err_off

print(off_ref)
print(on_ref)


fig, ax = plt.subplots(figsize=(8, 6))

# creating a subplot with no data to display the legend
gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

# plot the varaible source when its off
for survey in on_ref['survey_name'].unique():
        survey_data = on_ref[on_ref['survey_name'] == survey]
        ax1.errorbar(survey_data['mjd'].values, survey_data['flux_ref_norm'].values, yerr=survey_data['flux_err_ref'].values, fmt='.', color=survey_data['color'].iloc[0], label=survey, zorder=2)

# plot the variable source when its off
for survey in off_ref['survey_name'].unique():
        survey_data = off_ref[off_ref['survey_name'] == survey]
        ax1.errorbar(survey_data['mjd'].values, survey_data['flux_ref_norm'].values, yerr=survey_data['flux_err_ref'].values, marker="v", color=survey_data['color'].iloc[0], label=survey, zorder=2, linestyle='none')

# set the labels and title
ax1.set_xlabel('Frequency [Hz]')
ax1.set_xlabel('Date [MJD]')
ax1.set_ylabel('Fractional Variation %')
ax1.set_title(args.source_name + ' lightcurve')

# add legend to ax2
handles, labels = ax1.get_legend_handles_labels()
ax2.legend(handles, labels, loc='center', frameon=False)
ax2.axis('off')

#Saving the plot
if args.fractional_variation is None:
    plt.show()
else:
    fig.savefig(args.fractional_variation)
