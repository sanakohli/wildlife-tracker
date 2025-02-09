# %%
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import json
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

input_df = pd.read_csv('data/input_df.csv')
input_df['num_obs_endangered_pctl'] = input_df['num_obs_endangered'].rank(
    pct=True)

print('len', len(input_df))
for col in input_df.columns:
    if 'yr_change' in col:
        input_df[col] = input_df[col] * 100
print(input_df.head().to_string())
print('len input df', len(input_df))


X = input_df[['5_yr_change_species', '1_yr_change_species',
              '5_yr_change_pop', '1_yr_change_pop', 'future_5_yr_change_species']]
X.dropna(inplace=True)
y = X['future_5_yr_change_species']
X.drop(columns=['future_5_yr_change_species'], inplace=True)

print(f'std dev of future 5 yr change species {y.std()}')
reg = LinearRegression().fit(X, y)
coef = pd.DataFrame({'feature': X.columns, 'coef': reg.coef_})
print(coef.head().to_string())
rmse = ((reg.predict(X) - y) ** 2).mean() ** .5
print(f'rmse using 5 and 1 yr changes, pred 5 yr change{rmse}')

X = input_df[['5_yr_change_species', '1_yr_change_species', '5_yr_change_pop',
              '3_yr_change_pop', '1_yr_change_pop', 'future_3_yr_change_species']]
X.dropna(inplace=True)
y = X['future_3_yr_change_species']
X.drop(columns=['future_3_yr_change_species'], inplace=True)

print(f'std dev of future 3 yr change species {y.std()}')
reg = LinearRegression().fit(X, y)
coef = pd.DataFrame({'feature': X.columns, 'coef': reg.coef_})
print(coef.head().to_string())
rmse = ((reg.predict(X) - y) ** 2).mean() ** .5
print(f'rmse using 5 ,3 and 1 yr changes, pred 3 yr change {rmse}')


X = input_df[['1_yr_change_species',
              '1_yr_change_pop', 'future_5_yr_change_species']]
X.dropna(inplace=True)
y = X['future_5_yr_change_species']
X = X[['1_yr_change_species', '1_yr_change_pop']]
reg2 = LinearRegression().fit(X, y)
coef = pd.DataFrame({'feature': X.columns, 'coef': reg2.coef_})
rmse = ((reg2.predict(X) - y) ** 2).mean() ** .5
print(f'rmse using 1 yr changes {rmse}')
# print(coef.head().to_string())

# %%

# random_grid = {'bootstrap': [True, False],
#                'max_depth': [2,3,4],
#                'max_features': ['auto', 'sqrt'],
#                'min_samples_leaf': [1, 2, 4],
#                'min_samples_split': [2, 5, 10],
#                'n_estimators': [100, 130, 150]}

X_rf = input_df[['5_yr_change_species', '1_yr_change_species', '5_yr_change_pop',
                 '1_yr_change_pop', '3_yr_change_species', '3_yr_change_pop', 'future_5_yr_change_species']]
X_rf.dropna(inplace=True)
y_rf = X_rf['future_5_yr_change_species']
X_rf.drop(columns=['future_5_yr_change_species'], inplace=True)
print(f'len X_rf {len(X_rf)}')
X_train, X_test, y_train, y_test = train_test_split(
    X_rf, y_rf, test_size=0.3, random_state=42)
rf = RandomForestRegressor(
    n_estimators=70, random_state=42, max_depth=3, min_samples_split=2)
# rf = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
rmse = root_mean_squared_error(y_test, y_pred)
print(f'std dev of future 5 yr change species {y_rf.std()}')
print(f'rmse random forest {rmse}')

gb = GradientBoostingRegressor(
    n_estimators=70, random_state=42, learning_rate=0.01, max_depth=3)
gb.fit(X_train, y_train)
y_pred = gb.predict(X_test)
rmse = root_mean_squared_error(y_test, y_pred)
print('rmse gradient boosting', rmse)

# %%


def gen_out_json(model, features, y_name, obs_weight=.3, growth_weight=.7):
    input_df = pd.read_csv('data/input_df.csv')
    # print(input_df.isnull().sum())
    for col in input_df.columns:
        if 'yr_change' in col:
            input_df[col] = input_df[col] * 100
    pred_df = input_df[input_df['base_year'] == 2023]
    print(f'len pred df {len(pred_df)}')
    pred_df.dropna(subset=features, inplace=True)
    X_pred = pred_df[features]
    print(f'len pred df {len(X_pred)}')

    y_pred = model.predict(X_pred)
    pred_df[y_name] = y_pred
    pred_df['danger_score'] = (pred_df[y_name] - pred_df[y_name].mean()) / \
        pred_df[y_name].std(ddof=0)
    pred_df['num_obs_z'] = (pred_df['num_obs_endangered'] -
                            pred_df['num_obs_endangered'].mean()) / pred_df['num_obs_endangered'].std(ddof=0)
    pred_df['danger_score'] = obs_weight * pred_df['num_obs_z'] + pred_df['danger_score'] * growth_weight
    pred_df['danger_score'] = pred_df['danger_score'].rank(pct=True, ascending=False)
    pred_df['county_state'] = pred_df.apply(
        lambda x: f"{x['county']}_{x['state_fips']}", axis=1)
    print(pred_df.head().to_string())
    out = {}
    for row in pred_df.itertuples():
        out[row.county_state] = row.danger_score
    with open('data/pred.json', 'w') as json_file:
        json.dump(out, json_file, indent=4)
    with open('frontend/src/data/pred.json', 'w') as json_file:
        json.dump(out, json_file, indent=4)


gen_out_json(gb, ['5_yr_change_species', '1_yr_change_species', '5_yr_change_pop',
             '1_yr_change_pop', '3_yr_change_species', '3_yr_change_pop'], 'future_3_yr_change_species')
# %%

state_fips = pd.read_json('data/state_mapping_fips.json', orient='index')
state_fips.reset_index(inplace=True)
state_fips.columns = ['fips', 'state']
state_fips['state'] = state_fips['state'].str.lower()
pred_df2 = pred_df.merge(state_fips, on='state')
pred_df2['county_state'] = pred_df2.apply(
    lambda x: f"{x['county']}_{x['fips']}", axis=1)
print(pred_df2.to_string())
# print(pred_df2[pred_df2['fips'].isnull()])
print('num null fips ', len(pred_df2[pred_df2['fips'].isnull()]))
pred_df2 = pred_df2[['county_state', 'danger_score']]
out = {}
for row in pred_df2.itertuples():
    out[row.county_state] = row.danger_score
with open('pred.json', 'w') as json_file:
    json.dump(out, json_file, indent=4)
# pred_df2.to_csv('data/pred_df.csv', index=False)
# %%
