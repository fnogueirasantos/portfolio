import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import os

# Fix the directory
current_directory = os.path.dirname(__file__)
dataset_path = os.path.join(current_directory, 'data', 'Database.csv')


class Etl:

    def __init__(self, dataset=pd.read_csv(dataset_path)):
        self.dataset = dataset
    
    def etl_treemap(self):
        df = self.dataset
        df = df.groupby(['Category', 'Product'])['Revenue'].sum().reset_index()
        return df
    
    def etl_map_state(self):
        df = self.dataset
        df = df.groupby(['State','State Name'])['Revenue'].sum().reset_index()
        df['Percentage'] = (df['Revenue'] / df['Revenue'].sum()) * 100
        return df
    
    def etl_barchart_table(self, select_column):
        df = self.dataset
        df_grouped = df.groupby([f'{select_column}'])[['Quantity Ordered', 'Revenue', 'Profit Margin']].sum().reset_index()
        df_grouped = df_grouped.sort_values(by='Revenue', ascending=False)
        df_grouped['Average Ticket'] = df_grouped['Revenue'] / df_grouped['Quantity Ordered']
        df_grouped['%Quantity Ordered'] = 100*df_grouped['Quantity Ordered'] / df_grouped['Quantity Ordered'].sum()
        df_grouped['%Revenue'] = 100*df_grouped['Revenue'] / df_grouped['Revenue'].sum()
        df_grouped['%Profit Margin'] = 100*df_grouped['Profit Margin'] / df_grouped['Profit Margin'].sum()
        df_grouped['%Average Ticket'] = 100*df_grouped['Average Ticket'] / df_grouped['Average Ticket'].sum()
        df_grouped = df_grouped[[f'{select_column}', 'Quantity Ordered', '%Quantity Ordered', 
                                'Revenue', '%Revenue', 'Profit Margin','%Profit Margin',
                                'Average Ticket','%Average Ticket']]
        
        #Table
        df_table = df_grouped.copy()
        df_table['Average Ticket'] = df_table['Average Ticket'].apply(lambda x: '{:,.0f}'.format(x) if pd.notna(x) else '')
        df_table['Revenue'] = df_table['Revenue'].apply(lambda x: '{:,.0f}'.format(x) if pd.notna(x) else '')
        df_table['Profit Margin'] = df_table['Profit Margin'].apply(lambda x: '{:,.0f}'.format(x) if pd.notna(x) else '')
        df_table['%Quantity Ordered'] = df_table['%Quantity Ordered'].apply(lambda x: "{:.2%}".format(x/100))
        df_table['%Revenue'] = df_table['%Revenue'].apply(lambda x: "{:.2%}".format(x/100))
        df_table['%Profit Margin'] = df_table['%Profit Margin'].apply(lambda x: "{:.2%}".format(x/100))
        df_table['%Average Ticket'] = df_table['%Average Ticket'].apply(lambda x: "{:.2%}".format(x/100))
        return df_grouped, df_table
    
    def etl_lineplot(self):
        df = self.dataset
        df['Date'] = pd.to_datetime(df['Date'])
        df['MonthYear'] = df['Date'].dt.to_period('M').astype(str)
        monthly_revenue = df.groupby('MonthYear')['Revenue'].sum().reset_index()
        monthly_revenue['CumulativeRevenue'] = monthly_revenue['Revenue'].cumsum()
        monthly_revenue['%MonthlyGrowth'] = monthly_revenue['CumulativeRevenue'].pct_change().apply(lambda x: "{:.2%}".format(x))
        monthly_revenue = monthly_revenue.replace(np.nan, 0.00)
        return monthly_revenue


if __name__ == "__main__":
    pass