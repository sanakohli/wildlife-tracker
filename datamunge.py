# %%
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
county_pop = county_pop[['STATEFP10','NAME10','NAMELSAD10','ssp225']]
# Plot the shapefile
# county_pop.plot()  # Basic plot
# plt.title("County Population Data")
# plt.show()

# %%
import geopandas as gpd # this library allows us to load .shp file into pandas df
import pandas as pd
# from shapely.geometry import Point
from tqdm import tqdm
from tqdm.auto import tqdm 
import plotly.express as px
tqdm.pandas()

# LOAD IN COUNTY GEOMETRY AND SPECIES DATA, MERGE ON LONG LAT IN COUNTY GEOM

shapefile_path = "popdynamics-us-county-level-pop-projections-sex-race-age-ssp-2020-2100-pop-total-sex-race-shp/county_projectios_Total_bySex_byRace/total_pop_proj/hauer_county_totpop_SSPs.shp"
counties = gpd.read_file(shapefile_path)
counties = counties[['NAME10','NAMELSAD10','STATEFP10','geometry']]
state_fips = pd.read_csv('data/state_fips.csv')
# print('counties df\n',counties.head().to_string())

species_data = pd.read_csv('data/species_data.csv', sep='\t')
species_data = species_data[['gbifID','species','countryCode','stateProvince','individualCount','decimalLatitude','decimalLongitude','year']]
print(species_data.head().to_string())
print('rows species data',len(species_data))    # Number of rows
species_data = gpd.GeoDataFrame(species_data, geometry=gpd.points_from_xy(species_data.decimalLongitude, species_data.decimalLatitude), crs=counties.crs)
species_county = gpd.sjoin(species_data, counties, how="left")
print(species_county.head().to_string())

# %%
species_county_merge = species_county.copy()
species_county_merge['STATEFP10'] = species_county_merge['STATEFP10'].fillna(0).astype(int)
species_county_merge = species_county_merge.merge(state_fips, left_on='STATEFP10', right_on='st')
non_match = species_county_merge[species_county_merge['stname'] != species_county_merge['stateProvince']]
# print('merge \n',species_county_merge[['stname','stateProvince']].head().to_string())
print('non matching states\n',non_match.head().to_string())
species_county_merge.to_csv('data/species_county_dirty.csv') # merged but lots of non important columns
# %%
# stname is based on lat and l=ong so more accurate
# stateProvince is direct from gbif data
species_county_merge.rename(columns={'stname':'state_geo','stateProvince':'state_obs'}, inplace=True)
print('state_geo null', species_county_merge['state_geo'].isnull().sum())
print('STATEFP10 null', species_county_merge['STATEFP10'].isnull().sum())
print('state_obs null', species_county_merge['state_obs'].isnull().sum())
# %%

county_species = species_county_merge.groupby(['NAME10','year','STATEFP10']).size().reset_index(name='species')
print('county_species df \n',county_species.head().to_string())
# print('unique state fips',county_species['STATEFP10'].unique())
# print(f'len unique fips {len(county_species["STATEFP10"].unique())}')
county_species.to_csv('data/county_species_annual.csv')
county_species['ct_state'] = county_species.apply(lambda x: f"{x['NAME10']}--{x['STATEFP10']}", axis=1)
yearly_change = []
# print(county_species.to_string())
for county_state in county_species['ct_state'].unique():
    county = county_state.split('--')[0]
    state_fips = county_state.split('--')[1]
    county_data = county_species[county_species['ct_state'] == county_state]
    county_data = county_data.sort_values('year')
    for year in range(2015,2025):
        if year in county_data['year'].values: # TODO: fill in gaps of each year by doing mean of previous and next year
            county_row = {'county':county, 'state_fips':county_data['STATEFP10'].values[0], 'num_obs_endangered':county_data['species'].values[0]}
            county_row['base_year'] = year
            species_yr = county_data[county_data['year'] == year]['species'].values[0]
            year_minus5 = year - 5
            year_minus3 = year - 3
            year_minus1 = year - 1
            year_plus5 = year + 5
            year_plus3 = year + 3
            for year_diff in [year_minus5, year_minus3, year_minus1]:
                diff = year - year_diff
                if year_diff in county_data['year'].values:
                    diff_species = county_data[county_data['year'] == year_diff]['species'].values[0]
                    county_row[f'{diff}_yr_change_species'] = (species_yr - diff_species) / diff_species
                else:
                    county_row[f'{diff}_yr_change_species'] = None
            for year_diff in [year_plus5, year_plus3]:
                diff = year_diff - year
                if year_diff in county_data['year'].values:
                    diff_species = county_data[county_data['year'] == year_diff]['species'].values[0]
                    county_row[f'future_{diff}_yr_change_species'] = (diff_species - species_yr) / species_yr
                else:
                    county_row[f'future_{diff}_yr_change_species'] = None
            if len(county_row.keys()) > 3:
                yearly_change.append(county_row)
yearly_change = pd.DataFrame(yearly_change)
print(f'len {len(yearly_change)}')
print(f'num unique counties {len(yearly_change["county"].unique())}')
print(yearly_change.head().to_string())
print('unique county state combos',yearly_change.groupby(['county', 'state_fips']).ngroups)
# %%
county_pop = pd.read_csv('data/county_populations.csv')
county_pop = county_pop[['STNAME_2019','STATE_2019', 'CTYNAME','CENSUS2010POP','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015','POPESTIMATE2016','POPESTIMATE2017','POPESTIMATE2018','POPESTIMATE2019','ESTIMATESBASE2020','POPESTIMATE2021','POPESTIMATE2022','POPESTIMATE2023']]
county_pop.rename(columns={'STNAME_2019':'STNAME','CENSUS2010POP':'2010POP','ESTIMATESBASE2020':'2020POP'}, inplace=True)

county_pop['CTYNAME'] = county_pop['CTYNAME'].str.replace(' County','')
for col in county_pop.columns:
    if 'POPESTIMATE' in col:
        county_pop = county_pop.rename(columns={col:f'{col[11:]}POP'})

yearly_change_pop = []
for county in county_pop['CTYNAME'].unique():
    county_data = county_pop[county_pop['CTYNAME'] == county]
    for year in range(2015,2024):
        county_row = {'county':county, 'base_year':year,'state_fips': county_data['STATE_2019'].values[0]}
        # population of county in year
        county_yr_pop = county_data[f'{year}POP'].values[0]
        for diff in [1, 3 ,5]:
            year_minus_diff = year - diff
            pop_diff_yr = county_data[f'{year_minus_diff}POP'].values[0] # population of county in year minus diff
            county_row[f'{diff}_yr_change_pop'] = (county_yr_pop - pop_diff_yr) / pop_diff_yr
            
        yearly_change_pop.append(county_row)

yearly_change_pop = pd.DataFrame(yearly_change_pop)
print(yearly_change_pop.head().to_string())
# %%
input_df = yearly_change.merge(yearly_change_pop, on=['county','state_fips','base_year'])
print(f'len {len(input_df)}')
print(f'num unique counties {len(input_df["county"].unique())}')
print(f'num unique county state combos {input_df.groupby(["county", "state_fips"]).ngroups}')
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
