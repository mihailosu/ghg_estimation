import sklearn
import cloudpickle
import category_encoders
import numpy as np

file = open("maize_fertilization/xgboost_fertilization_with_imputation_v1_model.pkl", "rb")

pipe = cloudpickle.load(file)

model = pipe['xgbregressor']

importances = model.feature_importances_

print(importances)
print(len(importances))
print("\n\nFeature indices sorted by importances:\n\n")
print(np.argsort(importances))