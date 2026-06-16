import pandas as pd
import requests
import time
import json
import os

df = pd.read_csv('_truth/bigquery/noaa_ny_stations.csv')
df['county_name'] = None
df['county_fips'] = None

# Cache file to avoid repeated API calls
cache_file = '_truth/bigquery/geocode_cache.json'
cache = {}
if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
        cache = json.load(f)

for idx, row in df.iterrows():
    if pd.notna(row['lat']) and pd.notna(row['lon']):
        coord_key = f"{row['lat']:.3f},{row['lon']:.3f}"
        
        if coord_key in cache:
            df.loc[idx, 'county_name'] = cache[coord_key]['county_name']
            df.loc[idx, 'county_fips'] = cache[coord_key]['county_fips']
        else:
            try:
                # Use OSM Nominatim reverse geocoding
                url = f"https://nominatim.openstreetmap.org/reverse?lat={row['lat']}&lon={row['lon']}&format=json&zoom=8"
                response = requests.get(url, headers={'User-Agent': 'ALMS-Mapper/1.0'})
                data = response.json()
                
                county_name = None
                if 'address' in data:
                    # Try to get county
                    if 'county' in data['address']:
                        county_name = data['address']['county']
                    elif 'city_district' in data['address']:
                        county_name = data['address']['city_district']
                
                if county_name:
                    df.loc[idx, 'county_name'] = county_name
                    cache[coord_key] = {'county_name': county_name, 'county_fips': None}
                    print(f"✓ {row['name'][:20]}: {county_name}")
                
                time.sleep(0.3)  # Respect rate limits
            except Exception as e:
                print(f"✗ {row['name'][:20]}: {e}")

# Save cache
with open(cache_file, 'w') as f:
    json.dump(cache, f)

matched = df['county_name'].notna().sum()
df.to_csv('_truth/bigquery/noaa_ny_stations_with_county.csv', index=False)
print(f"\n{'='*50}")
print(f"Matched {matched} of {len(df)} stations to counties")
print(f"HASH: $(sha256sum _truth/bigquery/noaa_ny_stations_with_county.csv)")
print("\nMatched stations:")
print(df[df['county_name'].notna()][['name', 'county_name']].to_string())
