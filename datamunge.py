# %%
from itertools import count
import geopandas as gpd # this library allows us to load .shp file into pandas df
import matplotlib.pyplot as plt

# Path to the shapefile
shapefile_path = "popdynamics-us-county-level-pop-projections-sex-race-age-ssp-2020-2100-pop-total-sex-race-shp/county_projectios_Total_bySex_byRace/total_pop_proj/hauer_county_totpop_SSPs.shp"

# Load the shapefile
county_pop = gpd.read_file(shapefile_path)

ssp = 2 # which ssp do we want to look at right now


print('rows',len(county_pop))    # Number of rows
print('columns',county_pop.columns)    # Column names
for col in county_pop.columns:     # drop columns that arent for this ssp
    if col.startswith('ssp'):
        if int(col[3]) != ssp:
            county_pop = county_pop.drop(columns=col)
print(county_pop.head().to_string())  # View the first few rows of the dataset
print(county_pop.crs)     # Check the coordinate reference system (CRS)
# Plot the shapefile
county_pop.plot()  # Basic plot
plt.title("County Population Data")
plt.show()

# %%
import geopandas as gpd # this library allows us to load .shp file into pandas df
import pandas as pd
# from shapely.geometry import Point
from tqdm import tqdm
from tqdm.auto import tqdm 
import plotly.express as px
tqdm.pandas()

shapefile_path = "popdynamics-us-county-level-pop-projections-sex-race-age-ssp-2020-2100-pop-total-sex-race-shp/county_projectios_Total_bySex_byRace/total_pop_proj/hauer_county_totpop_SSPs.shp"
counties = gpd.read_file(shapefile_path)
counties = counties[['NAME10','NAMELSAD10','STATEFP10','geometry']]
state_fips = pd.read_csv('data/state_fips.csv')
# print('counties df\n',counties.head().to_string())

species_data = pd.read_csv('data/species_data.csv', sep='\t')
print('rows species data',len(species_data))    # Number of rows
species_data = gpd.GeoDataFrame(species_data, geometry=gpd.points_from_xy(species_data.decimalLongitude, species_data.decimalLatitude), crs=counties.crs)
# print('species data \n',species_data.head().to_string())
species_county = gpd.sjoin(species_data, counties, how="left")

species_county['STATEFP10'] = species_county['STATEFP10'].fillna(0).astype(int)
species_county = species_county.merge(state_fips, left_on='STATEFP10', right_on='st')
non_match = species_county[species_county['stname'] != species_county['stateProvince']]
# print('merge \n',species_county[['stname','stateProvince']].head().to_string())
print('non matching states\n',non_match.head().to_string())
species_county.to_csv('data/species_county_dirty.csv') # merged but lots of non important columns
# %%

county_species = species_county.groupby(['NAME10','year','stateProvince']).size().reset_index(name='species')
county_species = county_species[county_species['stateProvince'].str.len() > 2]

county_species = county_species[~county_species['stateProvince'].str.contains('\(')]
county_species = county_species[~county_species['stateProvince'].str.contains('\/')]
county_species['stateProvince'] = county_species['stateProvince'].str.lower()
county_species['stateProvince'] = county_species['stateProvince'].str.replace('main hawaiian islands','hawaii')
county_species['stateProvince'] = county_species['stateProvince'].str.replace('oahu island','hawaii')
county_species['stateProvince'] = county_species['stateProvince'].str.replace('hawaii state','hawaii')
county_species['stateProvince'] = county_species['stateProvince'].str.replace('hawai`i','hawaii')



print(county_species['stateProvince'].unique())
county_species.to_csv('data/county_species_annual.csv')
county_species['ct_state'] = county_species['NAME10'] +'--' + county_species['stateProvince']
yearly_change = []
# print(county_species.to_string())
for county_state in county_species['ct_state'].unique():
    county = county_state.split('--')[0]
    state = county_state.split('--')[1]
    county_data = county_species[county_species['ct_state'] == county_state]
    county_data = county_data.sort_values('year')
    for year in range(2015,2025):
        if year in county_data['year'].values: # TODO: fill in gaps of each year by doing mean of previous and next year
            county_row = {'county':county, 'state':county_data['stateProvince'].values[0]}
            county_row['base_year'] = year
            species_yr = county_data[county_data['year'] == year]['species'].values[0]
            year_minus5 = year - 5
            year_minus1 = year - 1
            year_plus5 = year + 5
            if year_minus5 in county_data['year'].values:
                county_row['5_yr_change_species'] = (species_yr - county_data[county_data['year'] == year_minus5]['species'].values[0]) / county_data[county_data['year'] == year_minus5]['species'].values[0]
            else:
                county_row['5_yr_change_species'] = None
            if year_minus1 in county_data['year'].values:
                county_row['1_yr_change_species'] = (species_yr - county_data[county_data['year'] == year_minus1]['species'].values[0]) / county_data[county_data['year'] == year_minus1]['species'].values[0]
            else:
                county_row['1_yr_change_species'] = None
            if year_plus5 in county_data['year'].values:
                species_2021 = county_data[county_data['year'] == year_plus5]['species'].values[0]
                county_row['future_5_yr_change_species'] = (species_2021 - species_yr) / species_yr
            else:
                county_row['future_5_yr_change_species'] = None
            yearly_change.append(county_row)
yearly_change = pd.DataFrame(yearly_change)
print(f'len {len(yearly_change)}')
print(f'num unique counties {len(yearly_change["county"].unique())}')
print(yearly_change.head().to_string())
print(yearly_change.groupby(['county', 'state']).ngroups)
# %%
county_pop = pd.read_csv('data/county_populations.csv')
county_pop = county_pop[['STNAME_2019', 'CTYNAME','CENSUS2010POP','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015','POPESTIMATE2016','POPESTIMATE2017','POPESTIMATE2018','POPESTIMATE2019','ESTIMATESBASE2020','POPESTIMATE2021','POPESTIMATE2022','POPESTIMATE2023']]
county_pop.rename(columns={'STNAME_2019':'STNAME','CENSUS2010POP':'2010POP','ESTIMATESBASE2020':'2020POP'}, inplace=True)
county_pop['CTYNAME'] = county_pop['CTYNAME'].str.replace(' County','')
for col in county_pop.columns:
    if 'POPESTIMATE' in col:
        county_pop = county_pop.rename(columns={col:f'{col[11:]}POP'})
# print(county_pop.head().to_string())
yearly_change_pop = []
for county in county_pop['CTYNAME'].unique():
    county_data = county_pop[county_pop['CTYNAME'] == county]
    for year in range(2015,2024):
        county_row = {'county':county, 'base_year':year,'state': county_data['STNAME'].values[0].lower()}
        year_minus5 = year - 5
        year_minus1 = year - 1
        pop_yr = county_data[f'{year}POP'].values[0]
        county_row['5_yr_change_pop'] = (pop_yr - county_data[f'{year_minus5}POP'].values[0]) / county_data[f'{year_minus5}POP'].values[0]
        county_row['1_yr_change_pop'] = (pop_yr - county_data[f'{year_minus1}POP'].values[0]) / county_data[f'{year_minus1}POP'].values[0]
        yearly_change_pop.append(county_row)

yearly_change_pop = pd.DataFrame(yearly_change_pop)
print(yearly_change_pop.head().to_string())
# %%
input_df = yearly_change.merge(yearly_change_pop, on=['county','state','base_year'])
print(f'len {len(input_df)}')
print(f'num unique counties {len(input_df["county"].unique())}')
print(input_df.head(100).to_string())
input_df.to_csv('data/input_df.csv', index=False)
# %%
merge = px.scatter_geo(
    non_match.head(1000),
    lat="decimalLatitude",
    lon="decimalLongitude",
    hover_data=["stname", "stateProvince"],
    scope='usa'
    # hovertemplate="Species: %{species} <br> StateRight: %{stname}<br> StateLeft: %{stateProvince} <br> County: %{NAME10}",
    # zoom=3,
    # map_style="carto-positron"
    
)
merge.show()

# %%
