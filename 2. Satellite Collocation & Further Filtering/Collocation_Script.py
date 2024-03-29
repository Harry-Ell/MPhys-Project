#! /apps/jasmin/jaspy/mambaforge_envs/jaspy3.10/mf-22.11.1-4/envs/jaspy3.10-mf-22.11.1-4-r20230718/bin/python

# coding: utf-8

# In[1]:

from datetime import datetime, timedelta, time
import numpy as np
import pandas as pd
import xarray as xr
from scipy.spatial import KDTree
import argparse 
from glob import glob
# In[3]:
parser = argparse.ArgumentParser()
parser.add_argument("date", help="Date on which to start process", type=str)
parser.add_argument("hours", help="Number of hours to process", type=float)
parser.add_argument("File_type", help="Type of file, eg: 'Real', 'Fitted', 'UpperCounterFac', 'LowerCounterFac", type=str)
args = parser.parse_args()

StartDate = datetime.fromisoformat(args.date)
EndDate = StartDate + timedelta(hours=args.hours)
FileType = args.File_type

def main():
    def CollocationFunction(StartDate, EndDate, FileType):
        while StartDate < EndDate:
            d = StartDate
            print(d)
            try:
                TrimmedAdvectedEmissions = pd.read_csv(f'/gws/nopw/j04/eo_shared_data_vol2/scratch/AO12/{FileType}DataAdvected/{StartDate.year:04d}_{StartDate.month:02d}_{StartDate.day:02d}_{StartDate.hour:02d}:{StartDate.minute:02d}') 
                TrimmedAdvectedEmissions['jday'] = pd.to_datetime(TrimmedAdvectedEmissions['jday'])
                if 'Visible_Albedo' in TrimmedAdvectedEmissions.columns:
                    print(f'Data already collocated for {StartDate}')
                    StartDate += timedelta(hours = 1)
                    continue
                grouped_data = TrimmedAdvectedEmissions.groupby('jday')
                subsets = [group for _, group in grouped_data]
                new_groups = []
                
                while d < StartDate + timedelta(hours = 24, minutes = 1): # Increment date here by 1 in hour column
                    try:
                        newPath = glob(f'/gws/nopw/j04/eo_shared_data_vol1/satellite/seviri-orac/Data/{d.year:04d}/{d.month:02d}/{d.day:02d}/{d.hour:02d}/{d.year:04d}{d.month:02d}{d.day:02d}{d.hour:02d}{d.minute:02d}{d.second:02d}-ESACCI-L2_CLOUD-CLD_PRODUCTS-SEVIRI-MSG[1-4]-fv3.0.nc')[0]
                        cloud_ds = xr.open_dataset(newPath, decode_times=False)
                    
                        wh_seviri_finite = np.isfinite(cloud_ds.lon.data.ravel())
                        seviri_lonlat_tree = KDTree(np.stack([cloud_ds.lon.data.ravel()[wh_seviri_finite], cloud_ds.lat.data.ravel()[wh_seviri_finite]], -1))
                        
                        modified_fitted_group = None
                        
                        for group in subsets:
                            time_difference = abs(group['jday'].iloc[0] - d)
                            if time_difference < timedelta(minutes = 5): 
                                wh_emissions_finite = np.isfinite(group.lon.to_numpy())
                                dists, nearest_neighbours = seviri_lonlat_tree.query(np.stack([
                                    group.lon.to_numpy()[wh_emissions_finite], 
                                    group.lat.to_numpy()[wh_emissions_finite]
                                ], -1))
                              
                                wh_emissions_valid = wh_emissions_finite[~np.isnan(wh_emissions_finite)]
                                
                                # Retrieve all desired variables from the cloud_ds data frame
                                extracted_values1  = cloud_ds.lat.data.ravel()[wh_seviri_finite][nearest_neighbours]
                                extracted_values2  = cloud_ds.lon.data.ravel()[wh_seviri_finite][nearest_neighbours] 
                                extracted_values3  = cloud_ds.cot.data.ravel()[wh_seviri_finite][nearest_neighbours]
                                extracted_values4  = cloud_ds.cot_uncertainty.data.ravel()[wh_seviri_finite][nearest_neighbours]                   
                                extracted_values5  = cloud_ds.cer.data.ravel()[wh_seviri_finite][nearest_neighbours]
                                extracted_values6  = cloud_ds.cer_uncertainty.data.ravel()[wh_seviri_finite][nearest_neighbours]                    
                                extracted_values7  = cloud_ds.cwp.data.ravel()[wh_seviri_finite][nearest_neighbours]
                                extracted_values8  = cloud_ds.cwp_uncertainty.data.ravel()[wh_seviri_finite][nearest_neighbours]
                                extracted_values9  = cloud_ds.cth.data.ravel()[wh_seviri_finite][nearest_neighbours]
                                extracted_values10 = cloud_ds.cth_uncertainty.data.ravel()[wh_seviri_finite][nearest_neighbours]
                                extracted_values11 = cloud_ds.illum.data.ravel()[wh_seviri_finite][nearest_neighbours]
                                extracted_values12 = cloud_ds.cldtype.data.ravel()[wh_seviri_finite][nearest_neighbours]
                                extracted_values13 = cloud_ds.cloud_albedo_in_channel_no_1.data.ravel()[wh_seviri_finite][nearest_neighbours]
                                extracted_values14 = cloud_ds.cloud_albedo_uncertainty_in_channel_no_1.data.ravel()[wh_seviri_finite][nearest_neighbours]

                                # Update a copy of the group
                                modified_fitted_group = group.copy()
                                modified_fitted_group['pixel lat'] = np.nan                
                                modified_fitted_group['pixel lon'] = np.nan
                                modified_fitted_group['cot'] = np.nan
                                modified_fitted_group['cot_uncertainty'] = np.nan                
                                modified_fitted_group['cer'] = np.nan
                                modified_fitted_group['cer_uncertainty'] = np.nan
                                modified_fitted_group['cwp'] = np.nan                
                                modified_fitted_group['cwp_uncertainty'] = np.nan
                                modified_fitted_group['cth'] = np.nan
                                modified_fitted_group['cth_uncertainty'] = np.nan                
                                modified_fitted_group['illum'] = np.nan
                                modified_fitted_group['cloud_type'] = np.nan
                                modified_fitted_group['Visible_Albedo'] = np.nan      
                                modified_fitted_group['Albedo_Uncertainty'] = np.nan                                
                
                                modified_fitted_group.loc[wh_emissions_valid, 'pixel lat'] = extracted_values1
                                modified_fitted_group.loc[wh_emissions_valid, 'pixel lon'] = extracted_values2                
                                modified_fitted_group.loc[wh_emissions_valid, 'cot'] = extracted_values3
                                modified_fitted_group.loc[wh_emissions_valid, 'cot_uncertainty'] = extracted_values4
                                modified_fitted_group.loc[wh_emissions_valid, 'cer'] = extracted_values5
                                modified_fitted_group.loc[wh_emissions_valid, 'cer_uncertainty'] = extracted_values6
                                modified_fitted_group.loc[wh_emissions_valid, 'cwp'] = extracted_values7
                                modified_fitted_group.loc[wh_emissions_valid, 'cwp_uncertainty'] = extracted_values8
                                modified_fitted_group.loc[wh_emissions_valid, 'cth'] = extracted_values9
                                modified_fitted_group.loc[wh_emissions_valid, 'cth_uncertainty'] = extracted_values10
                                modified_fitted_group.loc[wh_emissions_valid, 'illum'] = extracted_values11
                                modified_fitted_group.loc[wh_emissions_valid, 'cloud_type'] = extracted_values12               
                                modified_fitted_group.loc[wh_emissions_valid, 'Visible_Albedo'] = extracted_values13
                                modified_fitted_group.loc[wh_emissions_valid, 'Albedo_Uncertainty'] = extracted_values14    
                                
                                # Append the modified group to the new list
                                new_groups.append(modified_fitted_group)
                                
                        #print(d)
                        d += timedelta(minutes=15)
                        
                    except (FileNotFoundError, IndexError):
                       # print('no data available for ' + str(d))
                        # Create a new group with NaN values
                        new_group = pd.DataFrame(columns=TrimmedAdvectedEmissions.columns)
                        new_group['jday'] = [d] * len(new_group)
                        new_group['cot'] = np.nan
                        new_group['cot_uncertainty'] = np.nan
                        new_groups.append(new_group)
                        d += timedelta(minutes=15)
            except FileNotFoundError:
                print(f'No data Available to collocate with for {StartDate}')
            
            # Concatenate the modified groups into a new DataFrame
            try:
                new_trimmed_advected_emissions = pd.concat(new_groups, ignore_index=True)
            #print(new_trimmed_advected_emissions)
                new_trimmed_advected_emissions.to_csv('/gws/nopw/j04/eo_shared_data_vol2/scratch/AO12/{}DataAdvected/{}_{}_{}_{}:{}'.format(FileType, str(StartDate.year), str(StartDate.month).zfill(2), str(StartDate.day).zfill(2), str(StartDate.hour).zfill(2), str(StartDate.minute).zfill(2))) 
               # print(f'Data for {StartDate} added')
                StartDate += timedelta(hours = 1)
            except ValueError:
               # print(f'Data for {StartDate} is empty')
                StartDate += timedelta(hours = 1)
    # In[ ]:
    
    CollocationFunction(StartDate, EndDate, FileType)
if __name__ == "__main__":
        main()
