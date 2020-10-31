import sklearn
import cloudpickle
import category_encoders
import numpy as np

file = open("maize_fertilization/xgboost_fertilization_with_imputation_v1_model.pkl", "rb")

pipe = cloudpickle.load(file)

model = pipe['xgbregressor']

importances = model.feature_importances_

with open('atributi.txt') as file:
    array = file.readlines()

importances = [ item for item in zip(importances, array)]

importances = sorted(importances, key=lambda x: x[0], reverse=True)

# print(array)

print(pipe)
print("\n\n")
print(importances)
print(len(importances))
print("\n\nFeature indices sorted by importances:\n\n")
# print(np.argsort(importances))

with open('bitnoce.txt', 'w') as f:
    for item in importances:
        f.write(f'{item[0]}, {item[1]}')
