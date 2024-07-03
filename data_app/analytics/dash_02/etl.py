import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Fix the directory
current_directory = os.path.dirname(__file__)
dataset_path = os.path.join(current_directory, 'data', 'Dataset.csv')

class Etl:

    def __init__(self, dataset=pd.read_csv(dataset_path)):
        self.dataset = dataset

    def etl_waterfall_dre(self, filter_company):
        df = self.dataset
        if filter_company != 'Consolidated':
            df = df[df['Company'] == filter_company]
        else:
            pass
        df = (df.groupby(['Account', 'OrderAccount'])
                             [['LastYear', 'Realized']].sum()
                             .reset_index()
                             .sort_values(by='OrderAccount')
                             .drop(columns=['OrderAccount']))
        df['Delta'] = df['Realized'] - df['LastYear']
        df_walk_dre = df[['Account', 'Delta']].loc[~df['Account'].str.contains('=\)')]
        df_walk_dre_append = df.copy().query('Account == "(=) Net Result"')
        df_walk_01 = df_walk_dre_append[['Account', 'LastYear']].rename(columns={'LastYear': 'Delta'})
        df_walk_01['Account'] = df_walk_01['Account'].replace('(=) Net Result', '(=) Net Result LastYear')
        df_walk_02 = df_walk_dre_append[['Account', 'Realized']].rename(columns={'Realized': 'Delta'})
        df_walk_02['Account'] = df_walk_02['Account'].replace('(=) Net Result', '(=) Net Result Realized')
        df_walk_dre_final = pd.concat([df_walk_01, df_walk_dre, df_walk_02], ignore_index=True)
        return df_walk_dre_final
    
    def etl_dre(self, filter_company, filter_resume):
        df = self.dataset
        if filter_company != 'Consolidated':
            df = df[df['Company'] == filter_company]
        else:
            pass
        df = (df.groupby(['Account', 'OrderAccount'])
                             [['LastYear', 'Realized']].sum()
                             .reset_index()
                             .sort_values(by='OrderAccount')
                             .drop(columns=['OrderAccount']))
        df['LastYear'] = pd.to_numeric(df['LastYear'], errors='coerce')
        df['LastYear'] = df.apply(lambda row: abs(row['LastYear']) if pd.notna(row['LastYear']) and row['LastYear'] < 0 else row['LastYear'], axis=1)
        df['Realized'] = pd.to_numeric(df['Realized'], errors='coerce')
        df['Realized'] = df.apply(lambda row: abs(row['Realized']) if pd.notna(row['Realized']) and row['Realized'] < 0 else row['Realized'], axis=1)
        df['Delta'] = df['Realized'] - df['LastYear']
        df['Delta%'] = round((df['Realized'] / df['LastYear'] - 1) * 100, 2)
        df['LastYear'] = df['LastYear'].apply(lambda x: '{:,.0f}'.format(x) if pd.notna(x) else '')
        df['Realized'] = df['Realized'].apply(lambda x: '{:,.0f}'.format(x) if pd.notna(x) else '')
        df['Delta'] = df['Delta'].apply(lambda x: '{:,.0f}'.format(x) if pd.notna(x) else '')
        if filter_resume == 'Resume':
            select_account = ['(=) Net Revenue', '(=) Gross Profit', '(=) EBITDA', '(=) Net Result']
            df = df.query(f'Account in {select_account}')
        else:
            pass
        return df
    
    def etl_sub_account(self, filter_sub_account, filter_company):
        df = self.dataset
        if filter_company != 'Consolidated':
            df = df[df['Company'] == filter_company]
        else:
            pass
        df = df[df['Account'] == filter_sub_account]
        df = df.groupby(['Sub Account', 'OrderAccount'])[['LastYear', 'Realized']].sum().abs().reset_index().sort_values(by='OrderAccount')
        df.drop(columns=['OrderAccount'], inplace=True)
        df['Delta'] = df['Realized'] - df['LastYear']
        df['Delta%'] = round(100 * (df['Realized'] / df['LastYear']-1),2)
        df_walk_dre = df[['Sub Account','Delta']]
        df_lastyear = pd.DataFrame({'LastYear': [df['LastYear'].sum()], 'Sub Account': [f'{filter_sub_account} LastYear']})
        df_lastyear.rename(columns={'LastYear':'Delta'},inplace=True)
        df_realized = pd.DataFrame({'Realized': [df['Realized'].sum()], 'Sub Account': [f'{filter_sub_account} Realized']})
        df_realized.rename(columns={'Realized':'Delta'},inplace=True)
        df_walk_dre_final = pd.concat([df_lastyear, df_walk_dre], ignore_index=True)
        df_walk_dre_final = pd.concat([df_walk_dre_final, df_realized], ignore_index=True)
        df['LastYear'] = df['LastYear'].apply(lambda x: '{:,.0f}'.format(x) if pd.notna(x) else '')
        df['Realized'] = df['Realized'].apply(lambda x: '{:,.0f}'.format(x) if pd.notna(x) else '')
        df['Delta'] = df['Delta'].apply(lambda x: '{:,.0f}'.format(x) if pd.notna(x) else '')
        return df, df_walk_dre_final
    
    def etl_cards(self):
        df = self.dataset
        filter_selected = ['(=) Net Revenue','(=) Gross Profit','(=) EBITDA', '(=) Net Result']
        df_card =  df.query(f'Account in {filter_selected}').groupby(['Account'])[['Realized','LastYear']].sum().abs().reset_index()
        df_card['Up%'] = (df_card['Realized'] / df_card['LastYear'])-1
        df_card['Up%'] = df_card['Up%'].apply(lambda x: "{:.2%}".format(x))
        df_card['Realized'] = df_card['Realized'].apply(lambda x: "{:,.0f}".format(x))
        ebitda_value = df_card.query('Account == "(=) EBITDA"')['Realized'].values[0]
        ebitda_perc = df_card.query('Account == "(=) EBITDA"')['Up%'].values[0]
        gross_profitt_value = df_card.query('Account == "(=) Gross Profit"')['Realized'].values[0]
        gross_profitt_perc = df_card.query('Account == "(=) Gross Profit"')['Up%'].values[0]
        net_revenue_value = df_card.query('Account == "(=) Net Revenue"')['Realized'].values[0]
        net_revenue_perc = df_card.query('Account == "(=) Net Revenue"')['Up%'].values[0]
        net_result_value = df_card.query('Account == "(=) Net Result"')['Realized'].values[0]
        net_result_perc = df_card.query('Account == "(=) Net Result"')['Up%'].values[0]
        return ebitda_value, ebitda_perc, gross_profitt_value, gross_profitt_perc, net_revenue_value, net_revenue_perc, net_result_value, net_result_perc
    
    def etl_walk_company(self, filter_column):
        df = self.dataset
        df = df[df['Account'] == filter_column]
        df_walk = df[['Company','Realized','LastYear']].groupby(['Company'])[['Realized','LastYear']].sum().reset_index()
        df_walk['Delta'] = df_walk['Realized'] - df_walk['LastYear']
        df_lastyear = pd.DataFrame({'LastYear': [df_walk['LastYear'].sum()], 'Company': [f'{filter_column} LastYear']})
        df_lastyear.rename(columns={'LastYear':'Delta'},inplace=True)
        df_realized = pd.DataFrame({'Realized': [df_walk['Realized'].sum()], 'Company': [f'{filter_column} Realized']})
        df_realized.rename(columns={'Realized':'Delta'},inplace=True)
        df_walk = df_walk[['Company','Delta']]
        df_walk_final = pd.concat([df_lastyear, df_walk], ignore_index=True)
        df_walk_final = pd.concat([df_walk_final, df_realized], ignore_index=True)
        return df_walk_final

    def etl_barchart(self, filter_column):
        df = self.dataset
        df = df[df['Account'] == filter_column]
        df = df.groupby(['Company'])['Realized'].sum().abs().reset_index()
        df = df.sort_values(by='Realized', ascending=False)
        df['Realized%'] = df['Realized'] / df['Realized'].sum()
        #Format
        df['Realized%'] = df['Realized%'].apply(lambda x: "{:.2%}".format(x))
        return df
    
    def etl_barchart_upper(self, filter_column):
        df = self.dataset
        df = df[df['Account'] == filter_column]
        df = df.groupby(['Company'])[['Realized','LastYear']].sum().abs().reset_index()
        df['Diff'] = df['Realized'] - df['LastYear']
        df['Up%'] = (df['Realized'] / df['LastYear'])-1
        df.drop(columns=['Realized','LastYear'], inplace=True)
        df['Up_Group'] = ['Positive' if x >= 0 else 'Negative' for x in df['Diff']]
        #format
        df['Up%'] = df['Up%'].apply(lambda x: "{:.2%}".format(x))
        return df


if __name__ == "__main__":
    pass