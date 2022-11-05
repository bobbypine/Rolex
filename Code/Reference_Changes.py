import pandas as pd

pd.set_option('display.max_columns', None)


def ref_changes(old_month, new_month, old_year, new_year):
    old = pd.read_excel(r'..\Models\All Rolex Models {}.{}.xlsx'.format(old_month, old_year), sheet_name='All Watches').sort_values('Reference')
    new = pd.read_excel(r'..\Models\All Rolex Models {}.{}.xlsx'.format(new_month, new_year), sheet_name = 'All Watches').sort_values('Reference')
    added = new.loc[~new.Reference.isin(old.Reference)].copy()
    added['Status'] = 'New'
    disc = old.loc[~old.Reference.isin(new.Reference)].copy()
    disc['Status'] = 'Discontinued'
    changes = pd.concat([added, disc])
    print(changes)


ref_changes(7, 11, 2022, 2022)