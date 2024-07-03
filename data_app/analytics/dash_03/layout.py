from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

style_card = {'width': '70%', 'backgroundColor': 'white', 'color': 'black'}

# Layout
def create_layout():
    return dbc.Container(
        [
            html.Br(),
            html.A(html.Button('Back'), href='/', style={'position': 'absolute', 'top': 5, 'left': 10}),
            html.A(html.H3('Dashboard - Technology Equipments Sales'), style={'position': 'absolute', 'top': 3, 'left': 100}),
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
                            style={'width': '100%', 'color': '#176612'}
                            , className="border-0"
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(id="card3"),
                            style={'width': '100%', 'color': '#224047'},
                            className="border-0"
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(id="card4"),
                            style={'width': '100%', 'color': '#1d1d81'},
                            className="border-0"
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(id="card5"),
                            style={'width': '100%', 'color': '#1d1d81'},
                            className="border-0"
                        )
                    ),
                ], style={'backgroundColor': 'white'}
            ),
            # Treemap and Map State Container
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Br(),
                            dcc.Graph(id='tree_map', config={'displayModeBar': False}),
                        ],
                        width=6,  # Adjust width as needed
                    ),
                    dbc.Col(
                        [
                            html.Br(),
                            dcc.Graph(id='map_state', config={'displayModeBar': False}),
                        ],
                        width=6,  # Adjust width as needed
                    ),
                    
                    # Table
                    dbc.Col(
                        children=[
                            html.Br(),
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        [
                                            html.H6("Quantify and Profit Margin"),
                                            html.Div([
                                                html.Label("Select Dimension"),
                                                dcc.Dropdown(
                                                    id='filter_axis',
                                                    options=[
                                                        {'label': 'Category', 'value': 'Category'},
                                                        {'label': 'Product', 'value': 'Product'},
                                                        {'label': 'State', 'value': 'State Name'},
                                                        {'label': 'DayRange', 'value': 'DayRange'}
                                                    ],
                                                    value='Category',
                                                    clearable=False,
                                                    style={'color': 'black'}
                                                )
                                            ]
                                            )
                                        ],style={'backgroundColor': '#040d15', 'color':'white','border': 'none'}
                                    ),
                                    dbc.CardBody(
                                        dash_table.DataTable(
                                            id='table',
                                            style_table={'height': '282px', 'overflowY': 'auto'},
                                            style_as_list_view=True,
                                            style_cell={'textAlign': 'left',
                                                        'overflow': 'hidden',
                                                        'textOverflow': 'ellipsis', },
                                            style_header={
                                                'backgroundColor': '#040d15',
                                                'fontWeight': 'bold',
                                                'color': 'white'
                                            },
                                            style_data={'border': '1px solid #080808'},
                                            export_format='xlsx',
                                        ),style={'backgroundColor': '#040d15', 'border': 'none'}
                                    ),
                                ],
                                body=False,
                            ),                      
                        ],
                        width=4
                    ),
                    html.Br(),
                    dbc.Col(
                        [
                            html.Br(),
                            dcc.Graph(
                                id="barchart",
                                config={'displayModeBar': False},
                                # style={'height': '390px'}  # Adjust the height as needed
                            ),
                        ],
                        width=4,  # Adjust width as needed
                    ),
                    dbc.Col(
                        [
                            html.Br(),
                            dcc.Graph(
                                id="barchart_tkm",
                                config={'displayModeBar': False},
                                # style={'height': '390px'}  # Adjust the height as needed
                            ),
                        ],
                        width=4,  # Adjust width as needed
                    ),
                    html.Br(),
                    dbc.Col(
                        [
                            html.Br(),
                            dcc.Graph(
                                id="lineplot_revenue",
                                config={'displayModeBar': False},
                                # style={'height': '390px'}  # Adjust the height as needed
                            ),
                        ],
                        width=8  # Adjust width as needed
                    ),
                    dbc.Col(
                        [
                            html.Br(),
                            dcc.Graph(
                                id="lineplot_grow_up",
                                config={'displayModeBar': False},
                                # style={'height': '390px'}  # Adjust the height as needed
                            ),
                        ],
                        width=4,  # Adjust width as needed
                    ),
                ],
            ),
            html.Br()
        ],
        fluid=True,  # Set fluid=True to make the container responsive
        style={'background-color': '#080808', 'color': 'white'},  # Dark background color for the container
    )
