from .etl import Etl
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Create an instance of the Etl class
etl_instance = Etl()

# Cards
df_cards = etl_instance.dataset

def format_number(n):
    # Define the suffixes and their corresponding values
    suffixes = ['', 'K', 'M', 'B', 'T']
    num = n
    # Initialize the index for the suffix
    i = 0
    # Loop to determine the appropriate suffix
    while num >= 1000 and i < len(suffixes) - 1:
        num /= 1000
        i += 1
    # Format the number to one decimal place and append the suffix
    formatted_number = f"{num:.0f}{suffixes[i]}"
    return formatted_number

# Calculate 
sales_amount = df_cards['Amount'].count()
total_revenue = df_cards['Revenue'].sum()
mean_ticket = round(total_revenue / sales_amount,2)
# Formatting
formatted_sales_amount = format_number(sales_amount)
formatted_total_revenue = format_number(total_revenue)
formatted_mean_ticket = f"${mean_ticket:,.2f}"



style_filter = {
    'width': '100%',  # Adjust the width of the card
    'height': '450px',  # Adjust the height of the card
    'backgroundColor': 'black',  # Set the background color of the card
    'color': 'black',  # Set the text color of the card
    'margin': '5px',  # Set margin on all sides of the card
    'padding': '1px',  # Set padding on all sides of the card
    'borderRadius': '5px',  # Set the border radius of the card
    'boxShadow': '2px 2px 5px 0px rgba(0,0,0,0.75)',  # Add a shadow effect to the card
    'textAlign': 'center',  # Align text content in the card
}

style_filter_smartphone = {
    'backgroundColor': 'black',  # Set the background color of the card
    'color': 'black',  # Set the text color of the card
    'margin': '5px',  # Set margin on all sides of the card
    'padding': '1px',  # Set padding on all sides of the card
    'borderRadius': '5px',  # Set the border radius of the card
    'boxShadow': '2px 2px 5px 0px rgba(0,0,0,0.75)',  # Add a shadow effect to the card
    'textAlign': 'center',  # Align text content in the card
}

# Define layout for screen
layout_screen = [
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H6('Dimension:', className='title', style={'color': 'white'}),
                dcc.Dropdown(
                    id='select_dimension',
                    options=[
                        {'label': 'Category', 'value': 'Category'},
                        {'label': 'Location', 'value': 'Location'},
                        {'label': 'Type of Product', 'value': 'Type of Product'},
                        {'label': 'Name of Day', 'value': 'Name of Day'},
                        {'label': 'Period of Month', 'value': 'Period of Month'},
                        {'label': 'Period of Day', 'value': 'Period of Day'},
                        {'label': 'Hour', 'value': 'Hour'},
                        {'label': 'Product', 'value': 'Product'},
                        
                    ],
                    value='Category',
                    clearable=False
                    ),
                    html.P(),
                    html.Br(),
            
                html.H6('Revenue:', className='title',style={'color': 'white'}),
                dbc.Card(
                dbc.CardBody(#id="card1",
                    f"💵 {formatted_total_revenue}"),
                    className="border-0"
                    ),
                html.Hr(),
                html.H6('Sales:', className='title',style={'color': 'white'}),
                dbc.Card(
                dbc.CardBody(#id="card1",
                    f"📈 {formatted_sales_amount}"),
                    className="border-0"
                    ),
                html.Hr(),
                html.H6('Mean Ticket:', className='title',style={'color': 'white'}),
                dbc.Card(
                dbc.CardBody(#id="card1",
                    f"💵 {formatted_mean_ticket}"),
                    className="border-0"
                    ),
                    ], style=style_filter),
        ], width={'size': 1, 'offset': 0, 'order': 0}),
        dbc.Col([
            dcc.Graph(id='barchart', config={'displayModeBar': False}),
            html.Br(),
            dcc.Graph(id='scatter', config={'displayModeBar': False}),
                ],width={'size': 6, 'offset': 0, 'order': 0}),
        dbc.Col([
            dcc.Graph(id='treemap', config={'displayModeBar': False}),
            html.Br(),
            dcc.Graph(id='lineplot', config={'displayModeBar': False}),
                ],width={'size': 5, 'offset': 0, 'order': 0}),
        ]),
        html.Br(),
]

# Define layout for smartphone
layout_smartphone = [
    dbc.Row([
        dbc.Col([
            html.H6('Dimension:', className='title'),
            dcc.Dropdown(
                    id='select_dimension',
                    options=[
                        {'label': 'Category', 'value': 'Category'},
                        {'label': 'Location', 'value': 'Location'},
                        {'label': 'Type of Product', 'value': 'Type of Product'},
                        {'label': 'Name of Day', 'value': 'Name of Day'},
                        {'label': 'Period of Month', 'value': 'Period of Month'},
                        {'label': 'Period of Day', 'value': 'Period of Day'},
                        {'label': 'Hour', 'value': 'Hour'},
                        {'label': 'Product', 'value': 'Product'},
                        
                    ],
                    value='Category',
                    clearable=False,
                ),
            ],
            style=style_filter_smartphone),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='barchart', config={'displayModeBar': False}),
                html.Br(),
                dcc.Graph(id='scatter', config={'displayModeBar': False}),
                html.Br(),
                dcc.Graph(id='treemap', config={'displayModeBar': False}),
                html.Br(),
                dcc.Graph(id='lineplot', config={'displayModeBar': False}),
                html.Br(),
            ],
        width={'size': 12, 'offset': 0, 'order': 0}),
    ]),
]

def update_layout(device):
    if device == 'screen':
        return layout_screen
    else:
        return layout_smartphone


def update_charts(selected_dimension):
    #Barchart
    df_barchart = etl_instance.etl_barchart(select_column=selected_dimension)
    # Barchart Revenue
    barchart = px.bar(
        df_barchart,
        x=selected_dimension,
        y='Revenue',
        #orientation='h',
        color_discrete_sequence=['#42f5f5'],
        title=f'Total Revenue by {selected_dimension}',
        custom_data=['Perc%', 'Revenue'],
        text='Perc%'  # Adding the percentage values as text on the bars
    )

    # Update layout for better visualization
    barchart.update_layout(
        title_font=dict(color='white'),
        xaxis=dict(color='white'),
        yaxis=dict(tickformat="$.2s",color='white'),
        xaxis_showgrid=False, 
        yaxis_showgrid=False,
        plot_bgcolor='#040d15',
        paper_bgcolor='#040d15',
        margin=dict(l=10, r=10, b=10, t=60),
        hoverlabel=dict(bgcolor='#ffffff'),
        hovermode='closest',
    )

    barchart.update_traces(
        texttemplate='%{text}%',  # Display text as percentage
        textposition='inside',   # Position the text outside the bars
        textfont=dict(color='black')  # Set the text font color
    )

    #Scatter
    df_scatter = etl_instance.etl_scatter(selected_dimension)
    scatter_fig = px.scatter(df_scatter, x='Amount', y='Revenue', 
                         title='Scatter Plot', color=selected_dimension,
                        size='Revenue',hover_data=['Product'])
    # Add layout settings directly when creating the Figure object
    scatter_fig.update_layout(
        title='Monthly Revenue',
        title_font=dict(color='white'),
        xaxis=dict(title='Amount', tickformat=",.0s", color='white', gridcolor='#292F56'), 
        yaxis=dict(title='Revenue', tickformat="$.2s", color='white', gridcolor='#292F56'),
        plot_bgcolor='#060d13',
        paper_bgcolor='#060d13',
        legend=dict(font=dict(color='white'))
    )

    #Treemap
    df_treemap = etl_instance.etl_treemap(selected_dimension)
    
    treemap = px.treemap(
        df_treemap,
        path=[selected_dimension] if selected_dimension == "Product" else [selected_dimension, 'Product'],
        values='Revenue',
        title=f'Treemap of Revenue by Category and Product',
        color='Revenue',  # Specify color scale based on the filter_value
        color_continuous_scale='Magma',  # Adjust the color scale as needed
        hover_data={
            'Revenue': False,  # Format Revenue with commas and two decimal places
            'Product': False,  # Include the Product in hover data
            selected_dimension: False
        }
    )

    # Update layout for better visualization
    treemap.update_layout(
        margin=dict(l=10, r=10, b=10, t=60),
        plot_bgcolor='#010b13',
        paper_bgcolor='#010b13',
        title_font=dict(color='white'),
    )

    # Manually add color bar title and tick values
    treemap.update_layout(
        coloraxis_colorbar=dict(
            title=dict(font=dict(color='white')),
            tickfont=dict(color='white'),
        )
    )

    #Lineplot
    df_lineplot = etl_instance.etl_lineplot()

    # Create Lineplot
    lineplot_revenue = go.Figure()

    # Add Revenue data
    lineplot_revenue.add_trace(
        go.Scatter(
            x=df_lineplot['Sale Date'],
            y=df_lineplot['Revenue'],
            mode='lines',
            line=dict(color='#42f5f5'),
            marker=dict(color='#0c6e4e'),
            name='Revenue'
            )
        )

    # Add layout settings directly when creating the Figure object
    lineplot_revenue.update_layout(
        title='Revenue Over time',
        title_font=dict(color='white'),
        xaxis=dict(title='Date', color='white',gridcolor='#292F56'), 
        yaxis=dict(title='Revenue', tickformat=",.2s", color='white',gridcolor='#292F56'),
        plot_bgcolor='#060d13',
        paper_bgcolor='#060d13',
        hovermode='closest',
        legend=dict(font=dict(color='white'))
    )

    # Add a trendline using linear regression
    z = np.polyfit(range(len(df_lineplot)), df_lineplot['Revenue'], 1)
    p = np.poly1d(z)

    lineplot_revenue.add_trace(go.Scatter(
        x=df_lineplot['Sale Date'], 
        y=p(range(len(df_lineplot))),
        mode='lines', 
        name='Trendline', 
        line=dict(color='red', dash='dash')
    ))

    lineplot_revenue.update_xaxes(
        rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=14, label="2w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=2, label="2m", step="month", stepmode="backward"),
                    dict(count=4, label="4m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                ]),
                bgcolor="white",
                activecolor='tomato',
                y=1.22,
                x=0.25
            )
    )

    return barchart, scatter_fig, treemap, lineplot_revenue
    
