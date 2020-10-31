from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

from ghg import GHGPredictor

predictor = GHGPredictor()

dataset_df = pd.read_csv("db-wheat.csv", index_col=0)

# print(dataset_df.iloc[1])

dataset_df_2 = dataset_df.drop(columns=['Area', 'Year', 'Crop', 'Previous crop'])
# print(dataset_df_2)

dataset = dataset_df_2.to_numpy()

# print(dataset)

X, Y = dataset[:, :-1], dataset[:, -1:]

# print(X)
# print(Y)

seed = 10
test_size = 0.2

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

# print(len(X_train))
# print(len(X_test))
# print(len(Y_train))
# print(len(Y_test))

model = XGBRegressor()
model.fit(X_train, Y_train)

# print(model)
print(dataset_df_2.columns)
print(model.feature_importances_)

# print(X_test.shape)
y_pred = model.predict(X_test)
# predictions = [round(value) for value in y_pred]

Y_test = map(lambda x: x[0], Y_test)
# print(Y_test)

res = zip(y_pred, Y_test)

# print(list(res))

ghg_predictor = GHGPredictor()

def predict(model, row):
    preds = []
    # print(row)
    # print(row.).shape)
    for perc in range(-10, 11):
        new_row = row.copy()
        row_copy = row.copy()

        # new_row = new_row.iloc[0]
        new_row = new_row.drop(labels=['Area', 'Year', 'Crop', 'Previous crop', 'Yield'])
        # print(new_row.labels)
        # new_row = new_row.tolist()

        # print(new_row)
        # print(type(new_row))
        nitrogen = new_row['N'] * ((100 + perc) / 100)

        new_row['N'] = nitrogen
        row_copy['N'] = nitrogen
        new_row = np.array([new_row])
        # print(new_row)
        pred = model.predict(new_row)


        row_df = pd.DataFrame([row_copy])

        fuel_ghg = predictor.fuel_ghg_emissions(row_df["Area"], unit="kg")
        
        fuel_ghg = fuel_ghg.values[0]

        ms_ghg = predictor.managed_soils_ghg(row_df['N'], row_df['Manure'], row_df['Area'], row_df['Crop'], row_df['Yield'])

        ms_ghg = ms_ghg.values[0]


        sum_ghg = fuel_ghg + ms_ghg

        area = row_df['Area'].iloc[0]
        # print(area)

        # print(sum_ghg)
        # print(row_df['N'])

        # print(sum_ghg)

        # GHG
        # fuel = ghg_predictor.fuel_ghg_emissions()

        preds.append([nitrogen, pred[0], sum_ghg])

        print('{:4}% | Yield: {:.2f} | Area {} | C02_ha {:.5f} | C02 {:.5f}'.format(100 + perc, pred[0], area, sum_ghg / area, sum_ghg))

    return preds

# accuracy = accuracy_score(Y_test, predictions)
# print("Accuracy: %.2f%%" % (accuracy * 100.0))

import random

rand_ind = random.randrange(0, len(dataset))
rand_row = dataset_df.iloc[rand_ind]
while rand_row['N'] == 0:
    rand_ind = random.randrange(0, len(dataset))
    rand_row = dataset_df.iloc[rand_ind]
# rand_row = rand_row[:-1]

preds = predict(model, rand_row)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()

n_amount = [x[0] for x in preds]
yield_p = [x[1] for x in preds]
ghg_p = [x[2] for x in preds]

color = 'tab:red'
ax1.set_xlabel('N')
ax1.set_ylabel('Yield (t)', color=color)
ax1.set_title(f'GHG and yield predictions (Area: {rand_row["Area"]} ha)')
ax1.plot(n_amount, yield_p, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('CO2 (kg)', color=color)  # we already handled the x-label with ax1
ax2.plot(n_amount, ghg_p, color=color)
ax2.tick_params(axis='y', labelcolor=color)

print(n_amount)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()


