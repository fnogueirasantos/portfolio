import numpy as np
import joblib
import os
import warnings
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, RadioField, SelectField, IntegerField

# Filter FutureWarnings to avoid cluttering the output
warnings.filterwarnings("ignore", category=FutureWarning)

class ModelRegresison:

    def __init__(self):
        # Fix the directory
        current_directory = os.path.dirname(__file__)
        ml_directory = os.path.join(current_directory, 'ml')

        # Load the trained model
        self.lasso_cv_model = joblib.load(os.path.join(ml_directory, 'lasso_model.joblib'))

        # Load the pre-processing steps
        self.polynomial_converter = joblib.load(os.path.join(ml_directory, 'polynomial_converter.joblib'))
        self.scaler = joblib.load(os.path.join(ml_directory, 'scaler.joblib'))
    
    def new_predict(self, age, bmi, smoker):
        # New data point
        new_x = np.array([[age, bmi, smoker]])

        # Transform the new data point with polynomial features
        new_x_poly_features = self.polynomial_converter.transform(new_x)

        # Scale the new data point using the same scaler
        Scaled_X_new = self.scaler.transform(new_x_poly_features)

        # Make predictions using the Lasso regression model
        y_pred_new = self.lasso_cv_model.predict(Scaled_X_new)

        return y_pred_new
    
class FeaturesRegression(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = SelectField('Sex',  choices=['F','M','NB'],validators=[DataRequired()])
    bmi = SelectField('BMI',  choices=[15,16,17,18,19,20,21,22,23,24,25,
                                       26,27,28,29,30,31,32,33,34,35,36,
                                       37,38,39,40],validators=[DataRequired()])
    children = SelectField('Children',  choices=[0,1,2,3,4,5,6],validators=[DataRequired()])
    smoker = RadioField('Smoker', choices=['Yes','No'], validators=[DataRequired()])
    submit = SubmitField('Predict')


