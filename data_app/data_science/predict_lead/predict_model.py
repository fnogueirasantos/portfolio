import numpy as np
import pandas as pd
import joblib
import os
import random
import warnings
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from wtforms import SubmitField, IntegerField

# Filter FutureWarnings to avoid cluttering the output
warnings.filterwarnings("ignore", category=FutureWarning)

class Model_Lead_Predict:

    def __init__(self):
        # Fix the directory
        current_directory = os.path.dirname(__file__)
        ml_directory = os.path.join(current_directory, 'ml')

        # Load the trained model
        self.regression_model = joblib.load(os.path.join(ml_directory, 'linear_regression_model.joblib'))

        # Load the pre-processing steps
        self.scaler = joblib.load(os.path.join(ml_directory, 'scaler.joblib'))
    
    def new_predict_simulation(self, target_converted_users, min_budget, max_budget):
            
        # Initialize an empty list to store the final dataframes
        df_preview = []
                    
        # Iterate over the range of budgets
        for budget in range(min_budget, max_budget):
            # Set the campaign expenditure to the current budget value
            new_campaign_expenditure = budget
                            
            # Reshape the campaign expenditure for prediction
            new_pred_reshaped = np.array(new_campaign_expenditure).reshape(1, -1)
                            
            # Scale the campaign expenditure using the loaded scaler
            Scaled_X_new = self.scaler.transform(new_pred_reshaped)
                            
            # Make predictions using the loaded model
            new_predictions = self.regression_model.predict(Scaled_X_new)
                            
            # Create a dataframe with the predictions
            df_output = pd.DataFrame(new_predictions, columns=['Number_of_views',
                                                                'Number_of_clicks',
                                                                'Converted_users']).astype(int)
                            
            # Assign the budget value to the dataframe
            df_output['Budget'] = budget
                            
            # Classify the dataframe based on whether the predicted converted users match the target
            if df_output['Converted_users'][0] == target_converted_users:
                df_output['Classifier'] = 'Target'
            else:
                df_output['Classifier'] = 'Out of Target'
                        
            # Append the dataframe to the list of final dataframes
            df_preview.append(df_output)
        # Concatenate all dataframes in the list
        final_df = pd.concat(df_preview, ignore_index=True)
        df_predict_json = final_df.drop_duplicates('Converted_users')
        df_predict_json = df_predict_json.to_json(orient='columns')
                    
        return df_predict_json, final_df

    
class Features_Lead_Predict(FlaskForm):
    target_converted_users = IntegerField('Target Converted Users', default=random.randint(2, 199), validators=[DataRequired(), NumberRange(min=1, max=500, message='Value must be between 1 and 500')])
    min_budget = IntegerField('Min Budget', default=50, validators=[DataRequired(), NumberRange(min=50, max=5000, message='Value must be between 50 and 5000')])
    max_budget = IntegerField('Max Budget', default=3000, validators=[DataRequired(), NumberRange(min=51, max=25000, message='Value must be between 51 and 25000')])
    submit = SubmitField('Predict')


