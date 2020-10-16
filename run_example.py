
import pandas as pd

from ghg import GHGPredictor

# Diesel consumption for tilling in Germany?
TRACTOR_DIESEL_PER_HECTARE = 70

predictor = GHGPredictor()

df = pd.read_excel("Database.xlsx", header = 1,index_col =0, skiprows = [2])

def calculate_emissions(df):
    # fuel_litres = df["Area"] * TRACTOR_DIESEL_PER_HECTARE

    fuel_ghg = predictor.fuel_ghg_emissions(df["Area"], unit="kg")

    ms_ghg = predictor.managed_soils_ghg(df["N"], df["Manure"], df["Area"], df["Crop"], df["Yield"])

    return fuel_ghg + ms_ghg
new_df = df[['Source', 'Parcel', 'Area', 'Latitude', 
             'Longitude', 'Year', 'Crop','Manure',
             'Fertiliser amount', 'N', 'P', 'K',
             'Yield', 'Planting date', 'Harvest date']]
new_df['emissions (kg) - field']  = calculate_emissions(df)
new_df['emissions (kg/ha)']       = new_df['emissions (kg) - field'] / new_df['Area']

new_df = new_df.round(2)

new_df.to_csv("db-ghg-5.min.csv")