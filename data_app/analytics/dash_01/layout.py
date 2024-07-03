# layouts.py
from dash import dcc, html
import dash_bootstrap_components as dbc

style_card = {'width': '70%', 'backgroundColor': 'white', 'color': 'black'}

def create_layout():
    return dbc.Container(
        [
            html.Br(),
            html.A(html.Button('Back'), href='/', style={'position': 'absolute', 'top': 5, 'left': 10}),
            html.A(html.H3('Dashboard - Airline Passenger Satisfaction'), style={'position': 'absolute', 'top': 3, 'left': 100}),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(id="card1"),
                            style=style_card, className="border-0"
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(id="card2"),
                            style=style_card, className="border-0"
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(id="card3"),
                            style={'width': '100%', 'color': '#176612'},
                            className="border-0"
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(id="card4"),
                            style={'width': '100%', 'color': '#737305'},
                            className="border-0"
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(id="card5"),
                            style={'width': '100%', 'color': '#d9200b'},
                            className="border-0"
                        )
                    ),
                ], style={'backgroundColor': 'white'}
            ),
            # First Line: Barchart 01 and Barchart 02
            dbc.Row(
                [
                    # Barchart Container
                    dbc.Col(
                        [
                            html.Br(),
                            html.P("Select Barchart Filter:", style={'text-align': 'center'}),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Age Group', 'value': 'AgeGroup'},
                                    {'label': 'Class', 'value': 'Class'},
                                    {'label': 'Customer Type', 'value': 'Customer Type'},
                                    {'label': 'Flight Distance Group', 'value': 'Flight Distance Group'},
                                    {'label': 'Gender', 'value': 'Gender'},
                                    {'label': 'Type of Travel', 'value': 'Type of Travel'}
                                ],
                                value='AgeGroup',
                                className="dbc",
                                id="acaoDropdown",
                                clearable=False,
                                style={
                                    'width': '400px',
                                    'color': 'black',
                                    'fontSize': '14px',
                                    'text-align': 'center',
                                    'margin': '0 auto'
                                }
                            ),
                            html.Br(),
                            dcc.Graph(id='barchart_count', config={'displayModeBar': False}),
                            html.Br(),
                            dcc.Graph(id='barchart_feature', config={'displayModeBar': False}),
                        ],
                        width=6,
                    ),
                    # Histogram and Table Container
                    dbc.Col(
                        [
                            html.Br(),
                            html.P("Select Histogram Filter:", style={'text-align': 'center'}),
                            dcc.Dropdown(
                                className="dbc",
                                id="secondDropdown",
                                clearable=False,
                                style={
                                    'width': '400px',
                                    'color': 'black',
                                    'fontSize': '14px',
                                    'text-align': 'center',
                                    'margin': '0 auto'
                                }
                            ),
                            html.Br(),
                            # Histogram
                            dcc.Graph(
                                id="plot_histogram",
                                config={'displayModeBar': False},
                                # style={'height': '390px'}  # Adjust the height as needed
                            ),
                            html.Br(),
                            # Chart mean of services
                            dcc.Graph(
                                id="barchart_services",
                                config={'displayModeBar': False},
                                # style={'height': '390px'}  # Adjust the height as needed
                            ),
                        ],
                        width=6,
                    ),
                ],
            ),
            html.Br()
        ],
        fluid=True,
        style={'background-color': '#001121', 'color': 'white'},
    )
