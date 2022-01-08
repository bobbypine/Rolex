from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd


def rolliefuzz(prior_month_number, current_month_number, prior_month_year, current_month_year):
    o_data = pd.read_csv(r'Rolex_AD_List_{}_{}.csv'.format(prior_month_number, prior_month_year))[
        ['Name', 'Address', 'City', 'State', 'ID']]
    n_data = pd.read_csv(r'Rolex_AD_List_{}_{}.csv'.format(current_month_number, current_month_year))[
        ['Name', 'Address', 'City', 'State', 'ID']]
    o_matched = []
    n_matched = []
    data = []
    for row in o_data.index:
        o_id_val = o_data._get_value(row, "ID")
        for columns in n_data.index:
            n_id_val = n_data._get_value(columns, 'ID')
            matched_token = fuzz.partial_ratio(o_id_val, n_id_val)
            if matched_token > 80:
                o_matched.append(o_id_val)
                n_matched.append(n_id_val)
                data.append([o_id_val, n_id_val, matched_token])
    openings = n_data.loc[~n_data.ID.isin(n_matched)][['Name', 'Address', 'City', 'State']]
    openings['Status'] = 'Opened'
    closings = o_data.loc[~o_data.ID.isin(o_matched)][['Name', 'Address', 'City', 'State']]
    closings['Status'] = 'Closed'
    changes = pd.concat([openings, closings])
    if len(changes) == 0:
        print('No Changes This Month')
    else:
        return changes


if __name__ == "__main__":
    rolliefuzz(12, 1, 2021, 2022)
