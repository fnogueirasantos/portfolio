import pandas as pd
import pickle
import os
import random
from wtforms import StringField, SubmitField, RadioField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
import warnings

# Filter FutureWarnings to avoid cluttering the output
warnings.filterwarnings("ignore", category=FutureWarning)

class ModelClasifier():

    def __init__(self):
        # Fix the directory
        current_directory = os.path.dirname(__file__)
        ml_directory = os.path.join(current_directory, 'ml')

        # Load the pre-processing steps
        self.scaler = pickle.load(open(os.path.join(ml_directory, 'scaler.sav'), 'rb'))

        # Load the trained model for each prediction
        self.xgboost = pickle.load(open(os.path.join(ml_directory, 'best_model.pkl'), 'rb'))
    
    def new_predict(self, features):

        # Convert features to DataFrame with an index
        new_data = pd.DataFrame(features, index=[0])

        # Encode categorical variables
        new_data['gender'] = new_data['gender'].map({'Female': 0, 'Male': 1})
        new_data['SeniorCitizen'] = new_data['SeniorCitizen'].map({'No': 0, 'Yes': 1})
        new_data['Partner'] = new_data['Partner'].map({'No': 0, 'Yes': 1})
        new_data['Dependents'] = new_data['Dependents'].map({'No': 0, 'Yes': 1})
        new_data['PhoneService'] = new_data['PhoneService'].map({'No': 0, 'Yes': 1})
        new_data['MultipleLines'] = new_data['MultipleLines'].map({'No': 0, 'Yes': 1, 'No phone service': 2})
        new_data['InternetService'] = new_data['InternetService'].map({'No': 0, 'DSL': 1, 'Fiber optic': 2})
        new_data['OnlineSecurity'] = new_data['OnlineSecurity'].map({'No': 0, 'Yes': 1, 'No internet service': 2})
        new_data['OnlineBackup'] = new_data['OnlineBackup'].map({'No': 0, 'Yes': 1, 'No internet service': 2})
        new_data['DeviceProtection'] = new_data['DeviceProtection'].map({'No': 0, 'Yes': 1, 'No internet service': 2})
        new_data['TechSupport'] = new_data['TechSupport'].map({'No': 0, 'Yes': 1, 'No internet service': 2})
        new_data['StreamingTV'] = new_data['StreamingTV'].map({'No': 0, 'Yes': 1, 'No internet service': 2})
        new_data['StreamingMovies'] = new_data['StreamingMovies'].map({'No': 0, 'Yes': 1, 'No internet service': 2})
        new_data['Contract'] = new_data['Contract'].map({'Month-to-month': 0, 'One year': 1, 'Two year': 2})
        new_data['PaperlessBilling'] = new_data['PaperlessBilling'].map({'No': 0, 'Yes': 1})
        new_data['PaymentMethod'] = new_data['PaymentMethod'].map({'Electronic check': 0, 'Mailed check': 1, 'Bank transfer (automatic)': 2, 'Credit card (automatic)': 3})

        for column in new_data.columns:
            if column != 'TotalCharges':
                new_data[column] = new_data[column].astype('int')
            else:
                new_data[column] = new_data[column].astype('float')

        # Scale the new data
        # Select only the columns you want to normalize
        columns_to_normalize = ['tenure', 'TotalCharges']
        new_data_to_normalize = new_data[columns_to_normalize]
        new_data_normalize = self.scaler.transform(new_data_to_normalize)
        new_data[columns_to_normalize] = new_data_normalize

        # Predict probabilities
        probability_values = self.xgboost.predict_proba(new_data.values) * 100

        # Convert the array to a DataFrame
        df_probability_values = pd.DataFrame(probability_values, columns=['Probability_Churn_No', 'Probability_Churn_Yes'])

        return df_probability_values

class FeaturesClassification(FlaskForm):

    # Define random values for each feature
    random_id = "Client - " + str(random.randint(0, 4000))
    random_gender = random.choice(['Male', 'Female'])
    random_senior_citizen = random.choice(['Yes', 'No'])
    random_partner = random.choice(['Yes', 'No'])
    random_dependents = random.choice(['Yes', 'No'])
    random_tenure = random.randint(1, 80)
    random_phone_service = random.choice(['Yes', 'No'])
    random_multiple_lines = random.choice(['Yes', 'No', 'No phone service'])
    random_internet_service = random.choice(['DSL', 'Fiber optic', 'No'])
    random_online_security = random.choice(['Yes', 'No', 'No internet service'])
    random_online_backup = random.choice(['Yes', 'No', 'No internet service'])
    random_device_protection = random.choice(['Yes', 'No', 'No internet service'])
    random_tech_support = random.choice(['Yes', 'No', 'No internet service'])
    random_streaming_tv = random.choice(['Yes', 'No', 'No internet service'])
    random_streaming_movies = random.choice(['Yes', 'No', 'No internet service'])
    random_contract = random.choice(['Month-to-month', 'One year', 'Two year'])
    random_paperless_billing = random.choice(['Yes', 'No'])
    random_payment_method = random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
    random_total_charges = round(random.uniform(18.80, 8500.00), 2)

    # Define form fields with default values as random values
    id = StringField('ID', default=random_id, validators=[DataRequired()])
    gender = RadioField('Gender', default=random_gender, choices=['Male', 'Female'], validators=[DataRequired()])
    senior_citizen = SelectField('Senior Citizen', default=random_senior_citizen, choices=['Yes', 'No'], validators=[DataRequired()])
    partner = SelectField('Partner', default=random_partner, choices=['Yes', 'No'], validators=[DataRequired()])
    dependents = SelectField('Dependents', default=random_dependents, choices=['Yes', 'No'], validators=[DataRequired()])
    tenure = StringField('Tenure', default=random_tenure, validators=[DataRequired()])
    phone_service = SelectField('Phone Service', default=random_phone_service, choices=['Yes', 'No'], validators=[DataRequired()])
    multiple_lines = SelectField('Multiple Lines', default=random_multiple_lines, choices=['Yes', 'No', 'No phone service'], validators=[DataRequired()])
    internet_service = SelectField('Internet Service', default=random_internet_service, choices=['DSL', 'Fiber optic', 'No'], validators=[DataRequired()])
    online_security = SelectField('Online Security', default=random_online_security, choices=['Yes', 'No', 'No internet service'], validators=[DataRequired()])
    online_backup = SelectField('Online Backup', default=random_online_backup, choices=['Yes', 'No', 'No internet service'], validators=[DataRequired()])
    device_protection = SelectField('Device Protection', default=random_device_protection, choices=['Yes', 'No', 'No internet service'], validators=[DataRequired()])
    tech_support = SelectField('Tech Support', default=random_tech_support, choices=['Yes', 'No', 'No internet service'], validators=[DataRequired()])
    streaming_tv = SelectField('Streaming TV', default=random_streaming_tv, choices=['Yes', 'No', 'No internet service'], validators=[DataRequired()])
    streaming_movies = SelectField('Streaming Movies', default=random_streaming_movies, choices=['Yes', 'No', 'No internet service'], validators=[DataRequired()])
    contract = SelectField('Contract', default=random_contract, choices=['Month-to-month', 'One year', 'Two year'], validators=[DataRequired()])
    paperless_billing = SelectField('Paperless Billing', default=random_paperless_billing, choices=['Yes', 'No'], validators=[DataRequired()])
    payment_method = SelectField('Payment Method', default=random_payment_method, choices=['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], validators=[DataRequired()])
    total_charges = StringField('Total Charges', default=random_total_charges, validators=[DataRequired()])
    submit = SubmitField('Predict')




