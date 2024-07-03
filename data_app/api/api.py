from flask import jsonify
import sqlite3
import joblib
import numpy as np
import pandas as pd
import joblib
import os
import warnings
# Filter FutureWarnings to avoid cluttering the output
warnings.filterwarnings("ignore", category=FutureWarning)

class APIBackend:

    def __init__(self):
        # Fix the directory
        current_directory = os.path.dirname(__file__)
        ml_directory = os.path.join(current_directory, 'ml')
        data_directory = os.path.join(current_directory, 'data')

        # Load the trained model
        self.model = joblib.load(os.path.join(ml_directory, 'model_SARIMA.joblib'))
        self.database = os.path.join(data_directory, 'pizza_sales.db')
        self.df_query = os.path.join(data_directory, 'queries.csv')
    
    def sales_predict(self):
        # Generate forecasts for the next 30 steps
        forecast = self.model.get_forecast(steps=30)
        
        # Access the predicted values
        predicted_values = forecast.predicted_mean
        
        # Convert predicted values to actual sales using exponential function
        predicts = np.exp(predicted_values)
        
        # Create a DataFrame with predicted sales and corresponding dates
        predicted_sales = pd.DataFrame({'Order_Date': pd.date_range(start='today', periods=30),
                                        'Total_Sales': predicts})
        
        # Return the results as JSON
        return jsonify(predicted_sales.to_dict(orient='records'))
    
    def get_data_pizza_sales(self, query_id):
        
        df_query = pd.read_csv(self.df_query)
        query_mapping = {1: df_query['Query'].values[0],
                        2: df_query['Query'].values[1],
                        3: df_query['Query'].values[2],
                        4: df_query['Query'].values[3],
                        5: df_query['Query'].values[4]}

        database = self.database
        query_to_execute = query_mapping.get(query_id)
        if query_to_execute is None:
            return jsonify({'error': 'Invalid query ID'})

        # Establish a connection to the SQLite database
        with sqlite3.connect(database) as conn:
            # Create a cursor object to execute SQL queries
            cur = conn.cursor()

            # Execute the query
            cur.execute(query_to_execute)

            # Fetch all results
            results = cur.fetchall()

            # Fetch column names from cursor description
            column_names = [desc[0] for desc in cur.description]

            # Convert results to a list of dictionaries with dynamic keys
            pizza_sales = [{column_names[i]: row[i] for i in range(len(column_names))} for row in results]

            # Close the cursor
            cur.close()

        # Return the results as JSON
        return jsonify(pizza_sales)
