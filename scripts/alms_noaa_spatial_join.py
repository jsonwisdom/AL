import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import requests
import io

# Load stations
stations = pd.read_csv('_truth/bigquery/noaa_ny_stations.csv')
stations['geometry'] = stations.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
stations_gdf = gpd.GeoDataFrame(stations, geometry='geometry', crs='EPSG:4326')

# Load NY counties from GeoJSON
url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
response = requests.get(url)
counties = gpd.read_file(io.StringIO(response.text))

# Filter to NY (state FIPS 36)
ny_counties = counties[counties['STATE'] == 36].copy()
ny_counties = ny_counties.to_crs('EPSG:4326')

# Spatial join
joined = gpd.sjoin(stations_gdf, ny_counties, how='left', predicate='within')
joined['county_name'] = joined['NAME']
joined['county_fips'] = joined['id'].astype(str).str.zfill(5)

result = joined[['name', 'state', 'lat', 'lon', 'county_name', 'county_fips']]
result.to_csv('_truth/bigquery/noaa_ny_stations_with_county.csv', index=False)
matched = result['county_name'].notna().sum()
total = len(result)
print(f"Matched {matched} of {total} stations to counties ({matched/total*100:.0f}%)")
print("\nFirst 10 matches:")
print(result[['name', 'county_name', 'county_fips']].head(10))
print(f"\nUnmatched stations: {total - matched}")
if total - matched > 0:
    print("\nUnmatched stations:")
    print(result[result['county_name'].isna()][['name', 'lat', 'lon']].head(5))
