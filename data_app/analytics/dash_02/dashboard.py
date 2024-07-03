from dash import Dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from .etl import Etl
from .layout import create_layout
from .callbacks import update_cards, update_charts, waterfall_dre, df_dre, get_sub_account
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import secrets

# Create an instance of the Etl class
etl_instance = Etl()

# Define the layout of the app
style_card = style={'width': '70%', 'backgroundColor': '#1c1e1c', 'color':'#fefdfd'}

def create_dashboard_02(server):
    dash_app2 = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server, url_base_pathname=f'/{secrets.token_hex(10)}/')
    
    # Set the layout
    dash_app2.layout = create_layout()

    #Callback Cards
    @dash_app2.callback(
            Output('card1', 'children'),
            Output('card2', 'children'),
            Output('card3', 'children'),
            Output('card4', 'children'),
            Input('filter_dre', 'value'),
        )
    def cards(filter_dre):
        return update_cards(filter_dre)

    #Callback chart Page 01
    @dash_app2.callback(
            Output('barchart_value', 'figure'),
            Output('barchart_percentage', 'figure'),
            Input('filter_dre', 'value'),
        )
    def charts(filter_dre):
        return update_charts(filter_dre)

    # Callback Waterfall DRE
    @dash_app2.callback(
        [Output('waterfall_dre', 'figure')],
        [Input('filter_company', 'value')]
    )
    def chart_waterfall_dre(filter_company):
        return waterfall_dre(filter_company)

    #Callback chart Page 02
    # Callback to update the DataTable columns and initial data
    @dash_app2.callback(
        [Output('dre_table', 'columns'),
        Output('dre_table', 'data')],
        [Input('filter_company', 'value'),
        Input('filter_resume', 'value')]
    )
    def table_df_dre(filter_company, filter_resume):
        return df_dre(filter_company, filter_resume)

    # Callback Sub_Account
    @dash_app2.callback(
        [Output('sub_account_table', 'columns'),
        Output('sub_account_table', 'data'),
        Output('water_fall_sub_account', 'figure')],
        [Input('filter_sub_account', 'value'),
        Input('filter_company', 'value')]
    )
    def table_sub_account(filter_sub_account, filter_company):
        return get_sub_account(filter_sub_account, filter_company)
    
    return dash_app2



