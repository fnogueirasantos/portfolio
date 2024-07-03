import numpy as np
import pandas as pd
import joblib
import os
import warnings
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
import random
from wtforms import FloatField, SubmitField, RadioField, SelectField, IntegerField

# Filter FutureWarnings to avoid cluttering the output
warnings.filterwarnings("ignore", category=FutureWarning)

class ModelBudgetMkt:

    def __init__(self):
        # Fix the directory
        current_directory = os.path.dirname(__file__)
        ml_directory = os.path.join(current_directory, 'ml')

        # Load the trained model
        self.model_budget_mkt = joblib.load(os.path.join(ml_directory, 'model_budget_mkt.joblib'))

        # Load the pre-processing steps
        self.scaler = joblib.load(os.path.join(ml_directory, 'scaler.joblib'))
        
        # Load df_importance
        self.df_importance = pd.read_csv(os.path.join(ml_directory, 'df_importance.csv'))
    
    def new_predict(self, new_data):
        # New data point
        values_list = list(new_data.values())

        # Reshape the values_list into a 2D array with 1 column
        values_array = np.array(values_list).reshape(-1, 1)

        # scaler
        new_data_scaled = self.scaler.transform(values_array)

        df_extract_importance = self.df_importance
        
        # Predict
        predicts = self.model_budget_mkt.predict(new_data_scaled)
	
	# Create Final DataFrame
        df_predict = pd.DataFrame(predicts, columns=['Budget'])
        Rmse_X_Mean = '8.36%'
        df_predict['Factor'] = float(Rmse_X_Mean.replace('%',''))/100
        df_predict['Min Budget'] = df_predict['Budget'] - (df_predict['Budget'] * df_predict['Factor'])
        df_predict['Max Budget'] = df_predict['Budget'] + (df_predict['Budget'] * df_predict['Factor'])
        del df_predict['Factor']
        df_predict['TV'] = df_extract_importance['TV'][0]
        df_predict['Billboards'] = df_extract_importance['Billboards'][0]
        df_predict['TV'] = df_extract_importance['TV'][0]
        df_predict['Google Ads'] = df_extract_importance['Google Ads'][0]
        df_predict['Social Media'] = df_extract_importance['Social Media'][0]
        df_predict['Affiliate Marketing'] = df_extract_importance['Affiliate Marketing'][0]
        df_predict['TV'] = df_predict['Budget'] * df_predict['TV']
        df_predict['Billboards'] = df_predict['Budget'] * df_predict['Billboards']
        df_predict['Google Ads'] = df_predict['Budget'] * df_predict['Google Ads']
        df_predict['Social Media'] = df_predict['Budget'] * df_predict['Social Media']
        df_predict['Affiliate Marketing'] = df_predict['Budget'] * df_predict['Affiliate Marketing']
        df_predict['Revenue Target'] = values_list
        df_predict['Period'] = list(range(1, 13))
	# Organize
        df_predict = df_predict[['Period','Revenue Target','Min Budget',
                                 'Max Budget','Budget','TV','Billboards',
		                'Google Ads','Social Media',
                                'Affiliate Marketing']]
        df_predict = df_predict * 1000

        def format_number(num):
                if abs(num) >= 1.0e9:
                        return "{:.2f} B".format(num / 1.0e9)
                elif abs(num) >= 1.0e6:
                        return "{:.2f} M".format(num / 1.0e6)
                elif abs(num) >= 1.0e3:
                        return "{:.2f} K".format(num / 1.0e3)
                else:
                        return "{:.2f}".format(num)
                
        df_predict = df_predict.applymap(format_number)
        df_predict['Period'] = list(range(1, 13))

        df_predict_json = df_predict.to_json(orient='columns')

        return df_predict, df_predict_json
    
class FeaturesBudgetMkt(FlaskForm):
        Period_01 = IntegerField('Target Revenue Period 01', default=random.uniform(680, 3600), validators=[DataRequired()])
        Period_02 = IntegerField('Target Revenue Period 02', default=random.uniform(680, 3600), validators=[DataRequired()])
        Period_03 = IntegerField('Target Revenue Period 03', default=random.uniform(680, 3600), validators=[DataRequired()])
        Period_04 = IntegerField('Target Revenue Period 04', default=random.uniform(680, 3600), validators=[DataRequired()])
        Period_05 = IntegerField('Target Revenue Period 05', default=random.uniform(680, 3600), validators=[DataRequired()])
        Period_06 = IntegerField('Target Revenue Period 06', default=random.uniform(680, 3600), validators=[DataRequired()])
        Period_07 = IntegerField('Target Revenue Period 07', default=random.uniform(680, 3600), validators=[DataRequired()])
        Period_08 = IntegerField('Target Revenue Period 08', default=random.uniform(680, 3600), validators=[DataRequired()])
        Period_09 = IntegerField('Target Revenue Period 09', default=random.uniform(680, 3600), validators=[DataRequired()])
        Period_10 = IntegerField('Target Revenue Period 10', default=random.uniform(680, 3600), validators=[DataRequired()])
        Period_11 = IntegerField('Target Revenue Period 11', default=random.uniform(680, 3600), validators=[DataRequired()])
        Period_12 = IntegerField('Target Revenue Period 12', default=random.uniform(680, 3600), validators=[DataRequired()])



