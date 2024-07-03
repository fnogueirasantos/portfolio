from .etl import Etl
from dash.dependencies import Input, Output
from .layout import create_layout
from .callbacks import update_barcharts, update_histogram, update_cards
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import dash_bootstrap_components as dbc
from dash import Dash
import secrets

# Assuming etl.Etl is your class
etl_instance = Etl()

def create_dashboard_01(server):
    dash_app1 = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server, url_base_pathname=f'/{secrets.token_hex(10)}/')
    
    # Set the layout
    dash_app1.layout = create_layout()

    @dash_app1.callback(
        Output('barchart_count', 'figure'),
        Output('barchart_feature', 'figure'),
        Output('secondDropdown', 'options'),
        Output('secondDropdown', 'value'),
        Input('acaoDropdown', 'value'),
    )
    def charts_barcharts(acaoDropdown):
        return update_barcharts(acaoDropdown)

    @dash_app1.callback(
        Output('plot_histogram', 'figure'),
        Output('barchart_services', 'figure'),
        Input('acaoDropdown', 'value'),
        Input('secondDropdown', 'value'),
    )
    def charts_histogram(acaoDropdown, secondDropdown):
        return update_histogram(acaoDropdown, secondDropdown)

    # Callback Cards
    @dash_app1.callback(
        Output('card1', 'children'),
        Output('card2', 'children'),
        Output('card3', 'children'),
        Output('card4', 'children'),
        Output('card5', 'children'),
        Input('acaoDropdown', 'value'),
        Input('secondDropdown', 'value'),
    )
    def charts_cards(acaoDropdown, secondDropdown):
        return update_cards(acaoDropdown, secondDropdown)
    
    return dash_app1

       
