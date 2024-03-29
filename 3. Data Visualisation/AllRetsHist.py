#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np
import pandas as pd
import os
import pathlib
from datetime import datetime, time, timedelta
from scipy import stats
import matplotlib.pyplot as plt
import textwrap


# In[12]:


data_path = pathlib.Path("/gws/nopw/j04/eo_shared_data_vol2/scratch/AO12")
# Use a nested list comprehension to generate the file paths for each month
Real_files = sorted(list((data_path/"RealDataAdvected").glob("2019_*")))
CFU_files = sorted(list((data_path/"UpperCounterFacDataAdvected").glob("2019_*")))
CFL_files = sorted(list((data_path/"LowerCounterFacDataAdvected").glob("2019__*")))
# Flatten the nested lists and concatenate the files
cf_df = pd.concat((pd.read_csv(f) for f in CFU_files + CFL_files), ignore_index=True)
real_df = pd.concat((pd.read_csv(f) for f in Real_files), ignore_index=True)


# In[13]:


time_of_obs_real = pd.to_datetime(real_df["jday"], format='mixed')
timestep_real = np.round(real_df["timestep"] * 4) / 4
time_of_emission_real = time_of_obs_real - timestep_real.astype("timedelta64[h]")
# Fitted
time_of_obs_cf = pd.to_datetime(cf_df["jday"], format='mixed')
timestep_cf = np.round(cf_df["timestep"] * 4) / 4
time_of_emission_cf = time_of_obs_cf - timestep_cf.astype("timedelta64[h]")


# In[14]:


# Real
wh_valid_real = np.logical_and.reduce([real_df["cer_uncertainty"] < 10, real_df["cer"] > 0, real_df["cer"] < 40, real_df["illum"] != 2,
                                         real_df["cot_uncertainty"] < 10, real_df["cot"] > 0, real_df["cot"] < 30, real_df["cwp_uncertainty"] < 10,
                                         real_df["cwp"] > 0, real_df["cwp"] < 100, real_df["cloud_type"] == 3, real_df['cth'] > 0.5, real_df['cth'] < 2.5, 
                                         real_df['cth_uncertainty'] < 2, real_df["timestep"] < 24,  real_df["illum"] == 1])
# Counterfactuals
wh_valid_cf = np.logical_and.reduce([cf_df["cer_uncertainty"] < 10, cf_df["cer"] > 0, cf_df["cer"] < 40, cf_df["illum"] != 2,
                                        cf_df["cot_uncertainty"] < 10, cf_df["cot"] > 0, cf_df["cot"] < 30, cf_df["cwp_uncertainty"] < 10,
                                        cf_df["cwp"] > 0, cf_df["cwp"] < 100, cf_df["cloud_type"] == 3, cf_df['cth'] > 0.5, cf_df['cth'] < 2.5, 
                                        cf_df['cth_uncertainty'] < 2, cf_df["timestep"] < 24, cf_df["illum"] == 1])


# In[15]:


cer_data = real_df["cer"][wh_valid_real]
cwp_data = real_df["cwp"][wh_valid_real]
cot_data = real_df["cot"][wh_valid_real]
cer_data_cf = cf_df["cer"][wh_valid_cf]
cwp_data_cf = cf_df["cwp"][wh_valid_cf]
cot_data_cf = cf_df["cot"][wh_valid_cf]


# In[16]:


fig, axs_real = plt.subplots(1, 3, figsize=(15, 6))
c1 = 'blue'
c2 = 'red'
# Plot 'cer' on the existing subplot
n_cer, bins_cer, _ = axs_real[0].hist(cer_data, bins=np.linspace(0, 20, 81), density=True, color=c1, edgecolor='black', alpha=0.9, label='AIS')
n_cer_cf, bins_cer_cf, _ = axs_real[0].hist(cer_data_cf, bins=np.linspace(0, 20, 81), density=True, color=c2, edgecolor='black', alpha=0.9, label='Background')
axs_real[0].set_title('CER Real vs Background', fontname='serif', fontsize=16)
axs_real[0].set_xlabel('Cloud Droplet Effective Radius (CER), [$\mu m$]', fontname='serif', fontsize=16)
axs_real[0].set_ylabel('Probability Density', fontname='serif', fontsize=16)
axs_real[0].set_xticks([0, 5, 10, 15, 20])
axs_real[0].set_yticks([0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30], fontname='serif', fontsize=12, color='black')
legend0 = axs_real[0].legend(prop={'family': 'serif'}, fontsize=12)

# Plot 'cwp' on the existing subplot
n_cwp, bins_cwp, _ = axs_real[1].hist(cwp_data, bins=np.linspace(0, 80, 81), density=True, color=c1, edgecolor='black', alpha=0.9, label='AIS')
n_cwp_cf, bins_cwp_cf, _ = axs_real[1].hist(cwp_data_cf, bins=np.linspace(0, 80, 81), density=True, color=c2, edgecolor='black', alpha=0.9, label='Background')
axs_real[1].set_title('CWP Real vs Background', fontname='serif', fontsize=16)
axs_real[1].set_xlabel('Cloud Water Path (CWP), [$g/m^{2}$]', fontname='serif', fontsize=16)
axs_real[1].set_ylabel('Probability Density', fontname='serif', fontsize=16)
legend1 = axs_real[1].legend(prop={'family': 'serif'}, fontsize=12)

# Plot 'cot' on the existing subplot
n_cot, bins_cot, _ = axs_real[2].hist(cot_data, bins=np.linspace(0, 25, 81), density=True, color=c1, edgecolor='black', alpha=0.9, label='AIS')
n_cot_cf, bins_cot_cf, _ = axs_real[2].hist(cot_data_cf, bins=np.linspace(0, 25, 81), density=True, color=c2, edgecolor='black', alpha=0.9, label='Background')
axs_real[2].set_title('COT Real vs Background', fontname='serif', fontsize=16)
axs_real[2].set_xlabel('Cloud Optical Thickness (COT)', fontname='serif', fontsize=16)
axs_real[2].set_ylabel('Probability Density', fontname='serif', fontsize=16)
legend2 = axs_real[2].legend(prop={'family': 'serif'}, fontsize=12)

# Adjusting the border thickness for all subplots
for ax in axs_real:
    ax.spines['top'].set_linewidth(1.5)
    ax.spines['right'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)

# Adding a black box around each legend
for legend in [legend0, legend1, legend2]:
    frame = legend.get_frame()
    frame.set_edgecolor('black')
    frame.set_linewidth(2)  # Adjust the thickness of the legend box border

plt.tight_layout()
plt.savefig('2D_CER_V_TIME_V_TIME_UNCLEANED', bbox_inches='tight', dpi = 400)
plt.show()


# In[ ]:




