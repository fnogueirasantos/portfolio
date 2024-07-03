import plotly.graph_objects as go
from .etl import Etl
import plotly.express as px
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# Create an instance of the Etl class
etl_instance = Etl()


def update_cards(filter_dre):
    # Assuming etl_instance.dataset is your DataFrame
    ebitda_value, ebitda_perc, gross_profitt_value, gross_profitt_perc, \
    net_revenue_value, net_revenue_perc, \
    net_result_value, net_result_perc = etl_instance.etl_cards()
    # Generate content for each card
    card_1_content = f"Net Revenue: {net_revenue_value} / {net_revenue_perc} Y&Y"
    card_2_content = f"Gross Profit: {gross_profitt_value} / {gross_profitt_perc} Y&Y"
    card_3_content = f"EBITDA: {ebitda_value} / {ebitda_perc} Y&Y"
    card_4_content = f"Net Result: {net_result_value} / {net_result_perc} Y&Y"
    return card_1_content, card_2_content, card_3_content, card_4_content

def update_charts(filter_dre):
    # Assuming etl_instance.dataset is your DataFrame
    df_barchart = etl_instance.etl_barchart(filter_dre)
    df_barchart_upper = etl_instance.etl_barchart_upper(filter_dre)


    # Barchart
    fig_barchart = px.bar(df_barchart, x='Company', y='Realized',
                        text=df_barchart['Realized%'],
                        labels={'Realized%': 'Realized Percentage'},
                        hover_data={'Realized%': True},
                        title=f'Realized By: {filter_dre}',
                        color_discrete_sequence=['#100a61']
                        )

    # Update layout for better visualization
    fig_barchart.update_layout(
        xaxis_title='Company',
        yaxis_title='Realized',
        hovermode='x unified',  # Show hover information for all points on the same x-axis category
        yaxis=dict(tickformat=",.0s"),  # Format y-axis tick labels with commas
        xaxis_showgrid=False,  # Set showgrid to False for x-axis
        yaxis_showgrid=False,  # Set showgrid to False for y-axis
        margin=dict(l=10, r=10, b=10, t=60),
        plot_bgcolor='#f0f0f0',  # Set the background color of the plot
        paper_bgcolor='#f0f0f0'  # Set the background color of the entire chart area
    )

    # Barchart Upper
    fig_barchart_upper = px.bar(df_barchart_upper, x='Company', y='Diff',
                text=df_barchart_upper['Up%'],
                labels={'Up%': 'Realized Percentage'},
                hover_data={'Up%': True},
                title=f'Y&Y Growth or Reduction By: {filter_dre}',
                color='Up_Group',
                color_discrete_map={"Positive": "green", "Negative": "red"},
                )
    # Update layout for better visualization
    fig_barchart_upper.update_layout(
        xaxis_title='Company',
        yaxis_title='',
        hovermode='x unified',  # Show hover information for all points on the same x-axis category
        yaxis=dict(tickformat=",.0s"),  # Format y-axis tick labels with commas
        xaxis_showgrid=False,  # Set showgrid to False for x-axis
        yaxis_showgrid=False,  # Set showgrid to False for y-axis
        margin=dict(l=10, r=10, b=10, t=60),
        plot_bgcolor='#f0f0f0',  # Set the background color of the plot
        paper_bgcolor='#f0f0f0'  # Set the background color of the entire chart area
    )
    # Remove legend
    fig_barchart_upper.update_traces(showlegend=False)

    return fig_barchart, fig_barchart_upper

def waterfall_dre(filter_company):
    df_waterfall_dre = etl_instance.etl_waterfall_dre(filter_company)

    # Create a waterfall chart with the normalized Delta
    fig_waterfall_dre = go.Figure(go.Waterfall(
        x=list(df_waterfall_dre['Account']),
        measure=['absolute'] + ['relative'] * (len(df_waterfall_dre) - 2) + ['total'],
        y=(df_waterfall_dre['Delta']),  # Round to the nearest whole number
        base=0,
        decreasing={"marker": {"color": "red", "line": {"color": "red", "width": 0.3}}},
        increasing={"marker": {"color": "Teal","line": {"color": "green", "width": 0.3}}},
        totals={"marker": {"color": "#100a61", "line": {"color": "#100a61", "width": 0.3}}}
    ))
    fig_waterfall_dre.update_layout(
        title="Profit and Loss Statement",
        waterfallgap=0.3,
        margin=dict(l=10, r=10, b=10, t=60),
        xaxis=dict(color='white', gridcolor='#292F56'), 
        yaxis=dict(color='white', gridcolor='#292F56'),
        plot_bgcolor='#010b13',
        paper_bgcolor='#010b13',
        title_font=dict(color='white')
    )
    return [fig_waterfall_dre]  # Wrap the Figure object in a list

def df_dre(filter_company, filter_resume):
    df_dre = etl_instance.etl_dre(filter_company, filter_resume)
    columns = [{'name': col, 'id': col} for col in df_dre.columns]
    data = df_dre.to_dict('records')
    return columns, data

def get_sub_account(filter_sub_account, filter_company):
    df, walk = etl_instance.etl_sub_account(filter_sub_account, filter_company)
    
    # Table
    table_columns = [{'name': col, 'id': col} for col in df.columns]
    table_data = df.to_dict('records')

    # Set of legend positive or negative values
    sub_account = ['(+) Gross Revenue']
    if filter_sub_account in sub_account:
        d_results={"marker": {"color": "red", "line": {"color": "red", "width": 0.3}}}
        i_results={"marker": {"color": "teal", "line": {"color": "green", "width": 0.3}}}
    else:
        i_results={"marker": {"color": "red", "line": {"color": "red", "width": 0.3}}}
        d_results={"marker": {"color": "teal", "line": {"color": "green", "width": 0.3}}}

    # Waterfall Chart
    fig_waterfall_sub_account = go.Figure(go.Waterfall(
        x=list(walk['Sub Account']),
        measure=['absolute'] + ['relative'] * (len(walk) - 2) + ['total'],
        y=walk['Delta'],
        base=0,
        decreasing=d_results,
        increasing=i_results,
        totals={"marker": {"color": "#100a61", "line": {"color": "#100a61", "width": 0.3}}}
    ))
    fig_waterfall_sub_account.update_layout(
        title="Profit and Loss By Sub Account",
        waterfallgap=0.2,
        margin=dict(l=10, r=10, b=10, t=60),
        xaxis=dict(color='white', gridcolor='#292F56'), 
        yaxis=dict(color='white', gridcolor='#292F56'),
        plot_bgcolor='#010b13',
        paper_bgcolor='#010b13',
        title_font=dict(color='white'),
    )
    return table_columns, table_data, fig_waterfall_sub_account