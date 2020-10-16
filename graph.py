from ghg import GHGPredictor

import numpy as np

import pandas as pd

predictor = GHGPredictor()

def calculate_emissions(df):
    # fuel_litres = df["Area"] * TRACTOR_DIESEL_PER_HECTARE
    # print( * 11.4)

    fuel_ghg = predictor.fuel_ghg_emissions(df["Area"].astype(float), crop_type="wheat", unit="kg")

    ms_ghg = predictor.managed_soils_ghg(df["N"].astype(float), df["Manure"].astype(float), df["Area"].astype(float), df["Crop"], df["Yield"].astype(float))

    return fuel_ghg + ms_ghg
    # return ms_ghg

cols = ['Area', 'N', 'Manure', 'Crop', 'Yield']

area = 1.0
start_n = 0
n_step = 50
yld_t = 0

wheat = []
wheat_df = None
for i in range(0, 5):
    wheat.append([i, area, start_n + i * n_step, 0, 'wheat', yld_t])

wheat = np.array(wheat)
# print(wheat)
wheat_df = pd.DataFrame(columns=cols, index=wheat[:, 0], data=wheat[:, 1:])

print(wheat_df)

ems = calculate_emissions(wheat_df)

ems = (ems / 1000).round(4)

wheat_df['co2_t'] = ems

# print(wheat_df)

wheat_df.to_csv("wheat-example.csv")