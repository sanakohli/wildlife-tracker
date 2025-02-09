# %%
import pandas as pd
import json
from sklearn.linear_model import LinearRegression
input_df = pd.read_csv('data/input_df.csv')

print('len',len(input_df))
input_df.dropna(inplace=True)
input_df['future_5_yr_change_species'] = input_df['future_5_yr_change_species'] * 100
input_df['5_yr_change_species'] = input_df['5_yr_change_species'] * 100
input_df['1_yr_change_species'] = input_df['1_yr_change_species'] * 100
input_df['5_yr_change_pop'] = input_df['5_yr_change_pop'] * 100
input_df['1_yr_change_pop'] = input_df['1_yr_change_pop'] * 100
print(input_df.head().to_string())
print('len',len(input_df))



X = input_df[['5_yr_change_species','1_yr_change_species','5_yr_change_pop','1_yr_change_pop']]
y = input_df['future_5_yr_change_species']
reg = LinearRegression().fit(X, y)
coef = pd.DataFrame({'feature':X.columns,'coef':reg.coef_})
print(coef.head().to_string())
rmse = ((reg.predict(X) - y) ** 2).mean() ** .5
print(f'rmse {rmse}')

X = input_df[['1_yr_change_species','1_yr_change_pop']]
y = input_df['future_5_yr_change_species']
reg2 = LinearRegression().fit(X, y)
coef = pd.DataFrame({'feature':X.columns,'coef':reg2.coef_})
# print(coef.head().to_string())

# %%
input_df = pd.read_csv('data/input_df.csv')
input_df['5_yr_change_species'] = input_df['5_yr_change_species'] * 100
input_df['1_yr_change_species'] = input_df['1_yr_change_species'] * 100
input_df['5_yr_change_pop'] = input_df['5_yr_change_pop'] * 100
input_df['1_yr_change_pop'] = input_df['1_yr_change_pop'] * 100
pred_df = input_df[input_df['base_year'] == 2023]
print(f'len pred df {len(pred_df)}')
pred_df.dropna(subset=['5_yr_change_species','1_yr_change_species','5_yr_change_pop','1_yr_change_pop'], inplace=True)
X_pred = pred_df[['5_yr_change_species','1_yr_change_species','5_yr_change_pop','1_yr_change_pop']]
print(f'len pred df {len(X_pred)}')

y_pred = reg.predict(X_pred)
pred_df['predicted_5_yr_change_species'] = y_pred
pred_df['danger_score'] = pred_df['predicted_5_yr_change_species'].rank(pct=True, ascending=False)
print(pred_df.to_string())
# %%

state_fips = pd.read_json('data/state_mapping_fips.json', orient='index')
state_fips.reset_index(inplace=True)
state_fips.columns = ['fips','state']
state_fips['state'] = state_fips['state'].str.lower()
pred_df2 = pred_df.merge(state_fips, on='state')
pred_df2['county_state'] = pred_df2.apply(lambda x: f"{x['county']}_{x['fips']}", axis=1)
print(pred_df2.to_string())
# print(pred_df2[pred_df2['fips'].isnull()])
print('num null fips ',len(pred_df2[pred_df2['fips'].isnull()]))
pred_df2 = pred_df2[['county_state','danger_score']]
out = {}
for row in pred_df2.itertuples():
    out[row.county_state] = row.danger_score
with open('pred.json', 'w') as json_file:
    json.dump(out, json_file, indent=4)
# pred_df2.to_csv('data/pred_df.csv', index=False)
# %%
