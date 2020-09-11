import pandas as pd

from ghg import GHGPredictor

# Diesel consumption for tilling in Germany?
TRACTOR_DIESEL_PER_HECTARE = 70

predictor = GHGPredictor()

df = pd.read_csv("db.min.csv", index_col=0)

def calculate_emissions(df):
    fuel_litres = df["Area"] * TRACTOR_DIESEL_PER_HECTARE
    fuel_ghg = predictor.fuel_ghg_emissions(fuel_litres, unit="kg")

    ms_ghg = predictor.managed_soils_ghg(df["N"], df["Manure"], df["Area"])

    return fuel_ghg + ms_ghg

df['emissions (kg) - field'] = calculate_emissions(df)
df['emissions (kg/ha)'] = df['emissions (kg) - field'] / df['Area']

df = df.round(2)

df.to_csv("db-ghg.min.csv")