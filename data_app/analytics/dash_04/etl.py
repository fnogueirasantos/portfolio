import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import os

# Fix the directory
current_directory = os.path.dirname(__file__)
dataset_path = os.path.join(current_directory, 'data', 'Dataset.csv')

class Etl:

    def __init__(self, dataset = pd.read_csv(dataset_path)):

        self.dataset = dataset
    
    def etl_barchart(self, select_column):
        df = self.dataset
        df_barchart = df.groupby(select_column)['Revenue'].sum().reset_index()
        df_barchart['Perc%'] = round(100*df_barchart['Revenue'] / df_barchart['Revenue'].sum(),2)
        df_barchart.sort_values('Revenue',ascending=False, inplace=True)
        return df_barchart
    
    def etl_treemap(self, select_column):
        df = self.dataset
        if select_column == "Product":
            df_treemap = df.groupby([select_column])['Revenue'].sum().reset_index()
        else:
            df_treemap = df.groupby([select_column, 'Product'])['Revenue'].sum().reset_index()
        return df_treemap
    
    def etl_lineplot(self):
        df = self.dataset
        df_lineplot = df.groupby('Sale Date')['Revenue'].sum().reset_index()
        return df_lineplot
    
    def etl_scatter(self, select_column):
        df = self.dataset
        if select_column == "Product":
            df_scatter = df.groupby([select_column])[['Amount','Revenue']].sum().reset_index()
        else:
            df_scatter = df.groupby([select_column, 'Product'])[['Amount','Revenue']].sum().reset_index()
        return df_scatter

if __name__ == "__main__":
    pass