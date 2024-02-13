#! /apps/jasmin/jaspy/mambaforge_envs/jaspy3.10/mf-22.11.1-4/envs/jaspy3.10-mf-22.11.1-4-r20230718/bin/python
# coding: utf-8

# In[1]:


import numpy as np
import os 
import pathlib
from datetime import datetime, timedelta, time
import pickle
import numpy as np
import pandas as pd
import xarray as xr
import math
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("File_type", help="Real, Fitted, UpperCounterFac, LowerCounterFac", type=str)
args = parser.parse_args()
FileType = args.File_type

# In[2]:

def main():
    CERFile = np.zeros((24,24))
    CWPFile = np.zeros((24,24))
    # In[ ]:
    def Function(FileType):
        EndDate = datetime(2019, 7, 1, 0, 0)
        for i in range(0,24):
            for j in range(0, 24):
                StartDate = datetime(2019, 6, 1, 0, 0)
                
        # Empty dfs for cloud droplet effective radius
                File_data_cer =  []
        # Empty variables for assignment cer 
                mean_file_cer = 0        
        # Empty dfs for cloud liquid water path
                File_data_cwp = []
        # Empty variables for assignment cwp
                mean_file_cwp = 0
                
                while StartDate < EndDate:
                    try:
                        FileToRead = pd.read_csv(f'/gws/nopw/j04/eo_shared_data_vol2/scratch/AO12/{FileType}DataAdvected/{StartDate.year:04d}_{StartDate.month:02d}_{StartDate.day:02d}_{StartDate.hour:02d}:{StartDate.minute:02d}')
        # Making sure all time like variables are well behaved
                        FileToRead['jday'] = FileToRead['jday'].str.strip()
                        FileToRead['jday'] = pd.to_datetime(FileToRead['jday'], format='%Y-%m-%d %H:%M:%S', errors = 'coerce')
                  
        # Using floor functions to make conditioning easier inside of the conditions
                        FileToRead['jday']     = ((FileToRead['jday'].dt.hour).fillna(-1)).apply(lambda x: math.floor(x))
                        FileToRead['timestep'] = FileToRead['timestep'].apply(lambda x: math.floor(x))
                    
                        try:
                            condition1 = (FileToRead['jday'] == i) & (FileToRead['timestep'] == j) & (FileToRead['cer_uncertainty'] < 0.5 * FileToRead['cer']) & (FileToRead['cloud_type'] == 3)
                            condition2 = (FileToRead['jday'] == i) & (FileToRead['timestep'] == j) & (FileToRead['cwp_uncertainty'] < 0.5 * FileToRead['cwp']) & (FileToRead['cloud_type'] == 3)
                       
                        # Append the filtered 'Real' data to the lists
                            File_data_cer.extend(FileToRead[condition1]['cer'].to_numpy())                   
                            File_data_cwp.extend(FileToRead[condition2]['cwp'].to_numpy())
                      
                        except KeyError:
                            StartDate += timedelta(hours=1)
                            continue
                        StartDate += timedelta(hours=1)
                        #print(f'On {StartDate}, we add {len(Real_data_cer)} real, {len(Fitted_data_cer)} fitted, {len(Lower_counterfac_data_cer)} LCFC, and {len(Upper_counterfac_data_cer)} UCFC')
                    
                    except FileNotFoundError:
                        StartDate += timedelta(hours=1)
                        #print(f'Had to skip {StartDate}')  
                
        # Defining histograms 
                File_hist_cer, File_bins_cer = np.histogram(File_data_cer, bins=np.linspace(0, 40, 41), density=True)
                File_hist_cwp, File_bins_cwp = np.histogram(File_data_cwp, bins=np.linspace(0, 40, 41), density=True)
         
        # Defining their centres so we can evaluate means
                bin_centers = 0.5 * (File_bins_cer[1:] + File_bins_cer[:-1])        
                
        # Evaluating means and writing to associated 'heat maps'
                mean_file_cer             = np.sum(bin_centers * File_hist_cer)
                mean_file_cwp             = np.sum(bin_centers * File_hist_cwp)
                
                CERFile[i,j]   = mean_file_cer 
                CWPFile[i,j]   = mean_file_cwp  


        
    Function(FileType)
    np.save(f'CER_{FileType}_06', CERFile)
    np.save(f'CWP_{FileType}_06', CWPFile)
if __name__ =="__main__":
        main()
