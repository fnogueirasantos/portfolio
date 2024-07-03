from dash import dcc, html
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

style_title = {
    'height': '80px',  # Adjust the height of the card
    'backgroundColor': 'black',  # Set the background color of the card
    'color': 'white',  # Set the text color of the card
    'margin': '2px',  # Set margin on all sides of the card
    'padding': '1px',  # Set padding on all sides of the card
    'borderRadius': '5px',  # Set the border radius of the card
    'boxShadow': '2px 2px 5px 0px rgba(0,0,0,0.75)',  # Add a shadow effect to the card
    'textAlign': 'center',  # Align text content in the card
}

style_device = {
    'height': '80px',  # Adjust the height of the card
    'backgroundColor': 'black',  # Set the background color of the card
    'color': 'white',  # Set the text color of the card
    'margin': '2px',  # Set margin on all sides of the card
    'padding': '1px',  # Set padding on all sides of the card
    'borderRadius': '5px',  # Set the border radius of the card
    'boxShadow': '2px 2px 5px 0px rgba(0,0,0,0.75)',  # Add a shadow effect to the card
    'textAlign': 'center',  # Align text content in the card
}
# Layout
def create_layout():
    return html.Div([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.A(html.Button('Back'), href='/', style={'position': 'absolute', 'top': 5, 'left': 10}),
                html.H6('Device:', className='title'),
                dcc.RadioItems(
                    id='device-selector',
                    options=[
                        {'label': 'Screen', 'value': 'screen'},
                        {'label': 'Smartphone', 'value': 'smartphone'}
                    ],
                    value='screen',  # Default value
                    inline=True,
                    labelStyle={'display': 'inline-block'}
                ),
            ]),
            width={'size': 12},
            style=style_device
        ),
        dbc.Col(
            html.H3('Sales Coffee Dashboard', className='text-center mb-3 p-3'),
            width={'size': 12},
            style=style_title),
    ]),
    html.Div(id='layout-container')
])