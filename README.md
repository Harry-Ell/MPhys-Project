# Explanation of Functions

This is a repository for all of the Python scripts used for 'A012- Inferring Complex Process From Geostationary Satellites'. The input dataset is an array, with every point representing a spike in emissions, implying a polluted cloud pixel. Using ML these points are grouped, based on the best estimate of which correspond to the same ship track. This means our input is infact a long list of ship tracks in clouds, with a file for every day of the year in 2019. Each file contains a list of emissions spikes  The steps applied to this data set for cleaning and improving signal are as follows:
1. We fit the tracks with a least squares quadratic fit, and remove the signals which are below a cutoff R^2 value. These 'smoothed' ship tracks then are fitted with a smooth curve which is the best estimate of the 'actual' location of the ship/ the path it took. With the analytical curve, we can now form imaginary 'counterfactual' ships, 30km to either side of the actual ship path, always with instantaneously parallel bearing to the ship. It is these points which we use for sampling the 'unpolluted' cloud. Both of these steps occur in __________________________
2. These actual points, along with the fitted and counterfactual points are advected using HySplit data, carried out by Peter.
3. The new files, of which there is now one for every hour of every day in 2019, all contain the origional points, along with the advected positions for each point at 5 minute intervals for the following 24 hours. We want to trim these, to get rid of all points which are not at intervals of 15 minutes. This is because SEVIRI has 15 minute time resolution, and hence additional points are of no use to us. This, along with trimming all points which do not appear in the box (long, lat) = ([-16, 10], [-22, 0]). This is done by function 1 in the file _____________________
4. Function 2 in this same file is where we collocate with SEVIRI. This is done using a 2D KDTree, a 2D generalisation of a binary search algorithm. Cloud properties included are:
   1. Cloud droplet effective radius
   2. Cloud optical thickness
   3. Cloud liquid water path
   4. Cloud top heigh
   5. Illum (variable taking values 1,2,3 corresponding to day, twilight, night)
 5. Each of these are retrieved with an associated uncertainty, which is further used for data cleaning/ selection. 
      
