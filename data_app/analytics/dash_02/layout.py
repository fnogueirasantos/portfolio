from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Define the layout of the app

style_card = style={'width': '70%', 'backgroundColor': '#1c1e1c', 'color':'#fefdfd'}

def create_layout():
    return dbc.Container(
    fluid=True,
    style={'backgroundColor': '#505c59'},
    children=[
        html.Br(),
        html.A(html.Button('Back'), href='/', style={'position': 'absolute', 'top': 5, 'left': 10}),
        html.A(
            html.H3('Finance Dashboard'),
            style={
                'position': 'absolute',
                'top': 3,
                'left': 100,
                'color': 'white',
                'font-family': 'Arial',
            }
        ),
        html.Br(),
        dbc.Row([
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
                    style=style_card, className="border-0"
                )
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(id="card4"),
                    style=style_card, className="border-0"
                )
            ),
        ], style={'backgroundColor': '#1c1e1c'}),
        html.Br(),
        dcc.RadioItems(
            id='filter_dre',
            options=[
                {'label': label, 'value': label} for label in [
                    '(+) Gross Revenue', '(=) Net Revenue',
                    '(-) Cost of Goods/Services', '(=) Gross Profit',
                    '(-) Personnel Expenses', '(-) Administrative Expenses',
                    '(-) IT Expenses', '(-) Marketing and Sales Expenses',
                    '(-) General Expenses', '(=) EBITDA', '(=) Net Result'
                ]
            ],
            labelStyle={'display': 'inline-block'},
            value='(+) Gross Revenue',
            style={'width': '95%', 'margin': 'auto','backgroundColor': '#1c1e1c', 'color':'white'}  # Center horizontally
        ),
        html.Br(),
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id='barchart_value', 
                                       config={'displayModeBar': False})), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id='barchart_percentage', 
                                       config={'displayModeBar': False})), width=6)
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                children=[
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.H6("Statement of Income for the year"),
                                    html.Div(
                                        [
                                            html.Label("Select Filter"),
                                            dcc.Dropdown(
                                                id='filter_company',
                                                options=[
                                                    {'label': 'Consolidated', 'value': 'Consolidated'},
                                                    {'label': 'Aesthetics', 'value': 'Aesthetics'},
                                                    {'label': 'Building Material Store', 'value': 'Building Material Store'},
                                                    {'label': 'Clothes Store', 'value': 'Clothes Store'},
                                                    {'label': 'Drug Store', 'value': 'Drug Store'},
                                                    {'label': 'Goods Store', 'value': 'Goods Store'},
                                                ],
                                                value='Consolidated',
                                                clearable=False,
                                            ),
                                            html.Hr(),
                                            dcc.RadioItems(
                                                id='filter_resume',
                                                options=[
                                                    {'label': 'Resume', 'value': 'Resume'},
                                                    {'label': 'Complete', 'value': 'Complete'},
                                                ],
                                                value='Resume'
                                            ),
                                        ],
                                        className="mr-3",
                                    ),
                                ]
                            ),
                            dbc.CardBody(
                                dash_table.DataTable(
                                    id='dre_table',
                                    style_table={'height': '220px', 'overflowY': 'auto'},
                                    style_as_list_view=True,
                                    style_cell={'textAlign': 'left',
                                                'overflow': 'hidden',
                                                'textOverflow': 'ellipsis',},
                                    style_header={
                                        'backgroundColor': '#1c1e1c',
                                        'fontWeight': 'bold',
                                        'color': 'white'
                                    },
                                    style_data={'border': '1px solid #1c1e1c'},
                                    export_format='xlsx',
                                ),
                            ),
                        ],
                        body=True
                    )
                ],
                width=6
            ),
            dbc.Col(
                dbc.Card(
                    dcc.Graph(id='waterfall_dre',config={'displayModeBar': False}),
                    body=True,
                    style={'height': '500px'}  # Set the height of the dbc.Card
                ),
                width=6,
                style={'height': '500px'}  # Set the height of the dbc.Col
            ),
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                children=[
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.H6("Statement of Income for the year - Sub Account"),
                                    html.Div([
                                        html.Label("Select Filter"),
                                        dcc.Dropdown(
                                            id='filter_sub_account',
                                            options=[
                                                {'label': '(+) Gross Revenue', 'value': '(+) Gross Revenue'},
                                                {'label': '(-) Cost of Goods/Services', 'value': '(-) Cost of Goods/Services'},
                                                {'label': '(-) Personnel Expenses', 'value': '(-) Personnel Expenses'},
                                                {'label': '(-) Administrative Expenses', 'value': '(-) Administrative Expenses'},
                                                {'label': '(-) IT Expenses', 'value': '(-) IT Expenses'},
                                                {'label': '(-) General Expenses', 'value': '(-) General Expenses'}
                                            ],
                                            value='(-) Personnel Expenses',
                                            clearable=False,
                                        )
                                    ])
                                ]
                            ),
                            dbc.CardBody(
                                dash_table.DataTable(
                                    id='sub_account_table',
                                    style_table={'height': '312px', 'overflowY': 'auto'},
                                    style_as_list_view=True,
                                    style_cell={'textAlign': 'left',
                                                'overflow': 'hidden',
                                                'textOverflow': 'ellipsis',},
                                    style_header={
                                        'backgroundColor': '#1c1e1c',
                                        'fontWeight': 'bold',
                                        'color': 'white'
                                    },
                                    style_data={'border': '1px solid #1c1e1c'},
                                    export_format='xlsx',
                                ),
                            ),
                        ],
                        body=False
                    )
                ],
                width=6
            ),
            dbc.Col(
                dbc.Card(
                    dcc.Graph(id='water_fall_sub_account',config={'displayModeBar': False}),
                    body=True,
                    style={'height': '480px'}
                ),
                width=6
            ),
        ]),
        html.Br(),
    ]
)