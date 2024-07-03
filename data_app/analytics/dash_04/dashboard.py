from dash import Dash
import dash_bootstrap_components as dbc
from .etl import Etl
from .layout import create_layout
from .callbacks import update_layout, update_charts
from dash.dependencies import Input, Output
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import secrets


# Create an instance of the Etl class
etl_instance = Etl()


def create_dashboard_04(server):
    dash_app4 = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True, server=server, url_base_pathname=f'/{secrets.token_hex(10)}/')
    
    # Set the layout
    dash_app4.layout = create_layout()

    # Callbacks
    @dash_app4.callback(
    Output('layout-container', 'children'),
    [Input('device-selector', 'value')]
    )
    def select_layout(device):
        return update_layout(device)
        
    # Callbacks
    @dash_app4.callback(
        Output('barchart', 'figure'),
        Output('scatter', 'figure'),
        Output('treemap', 'figure'),
        Output('lineplot', 'figure'),
        [Input('select_dimension', 'value')]
        )
    def charts(selected_dimension):
        return update_charts(selected_dimension)       

    return dash_app4