# Explanation of Repository

'MPhys Project' is a repository for all the Python scripts and notebooks used in 'A012—Exploring Shipping-Induced Aerosol Influence on Cloud Evolution with Geostationary Satellites'. All folders 0--3 have .txt files in them which describe what each of the scripts/ notebooks do. 

The project begins with a dataset of GPS locations of ships. These are assumed to correspond to a spike in the emission of aerosols in this location. Using a Lagrangian approach, the now polluted parcel of air is followed along the flows of winds for the next 24 hours. Its location is recorded every 15 minutes. We refer to the set of locations on which the fluid parcel lands as its emission trajectory. 

Collocating with the SEVIRI instrument on board the geostationary satellite MSG, we retrieve cloud properties, such as liquid water content and mean droplet radius in clouds. This, along with the time since emission parameter attached to each point on the advection trajectory, allows us to plot how cloud properties change as a function of time since emission. 

Results of the project can be seen in '4. Results and Outputs' 
