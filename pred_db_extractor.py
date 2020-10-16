import pandas as pd

df = pd.read_csv("db.csv", index_col=0, skiprows=1)

cols = ['Source', 'Parcel', 'Area', 'Latitude', 'Longitude', 'Year', 'Crop',
        'Seed production', 'Variety', 'Previous crop', 'Seed units', 'Manure',
        'Fertiliser amount', 'N', 'P', 'K', 'Pesticide amount', 'Tillage',
        'Sowing', 'Fertiliser application', 'Pesticide application',
        'Irrigation', 'Harvest', 'Seed', 'Fertiliser', 'Pesticide', 'Yield',
        'Price', 'Revenue', 'Planting date', 'Harvest date']

cols_wanted = ['Area', 'Year', 'Crop', 'Previous crop', 'Manure','Fertiliser amount', 'N', 'P', 'K', 'Pesticide amount',  'Yield',]

cols_cost = ['Tillage',
       'Sowing', 'Fertiliser application', 'Pesticide application',
       'Irrigation', 'Harvest', 'Seed', 'Fertiliser', 'Pesticide',]

df_wheat = df.loc[df['Crop'].str.lower() == 'wheat']

# Select columns we want to train
df_workable = df_wheat[cols_wanted]

# Fill none
df_workable['Previous crop'] = df_workable['Previous crop'].fillna(value="No crop")

df_workable = df_workable.fillna(value=0.0)

# One hot encode categorical column
dummies = pd.get_dummies(df_workable['Previous crop']).add_prefix("prev_crop_")

df_workable = pd.concat([df_workable, dummies], axis=1)

yields = df_workable.pop("Yield")
df_workable['Yield'] = yields

df_workable.to_csv("db-wheat.csv")
