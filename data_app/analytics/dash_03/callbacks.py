from .etl import Etl
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Create an instance of the Etl class
etl_instance = Etl()

def update_charts(filter_axis):
    df_treemap = etl_instance.etl_treemap()
    df_map_state = etl_instance.etl_map_state()
    df_barchart_table, df_table = etl_instance.etl_barchart_table(filter_axis)
    df_lineplot = etl_instance.etl_lineplot()

    # Create a treemap
    treemap = px.treemap(
        df_treemap,
        path=['Category', 'Product'],
        values='Revenue',
        title='Treemap of Revenue by Category and Product',
        color='Revenue',  # You can specify a color scale based on revenue
        color_continuous_scale='Magma',  # Adjust the color scale as needed
    )
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

    # Create a choropleth map with Plotly Express
    map_state = px.choropleth(
        df_map_state,
        locations='State',
        locationmode='USA-states',
        color='Revenue',
        hover_data=['State Name', 'Revenue', 'Percentage'],
        scope='usa',
        title='Revenue by State',
        color_continuous_scale=px.colors.sequential.Teal,
    )

    # Customize the hover template
    map_state.update_traces(
        hovertemplate='%{customdata[0]}<br>%{customdata[1]:,.0f} USD<br>%{customdata[2]:.2f}%<extra></extra>')

    map_state.update_layout(
        geo=dict(
            scope='usa',
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'
        ),
        margin=dict(l=10, r=10, b=10, t=60),
        plot_bgcolor='#010b13',
        paper_bgcolor='#010b13',
        title_font=dict(color='white'),
    )
    # Manually add color bar title and tick values
    map_state.update_layout(
        coloraxis_colorbar=dict(
            title=dict(text='Revenue', font=dict(color='white')),
            tickfont=dict(color='white'),
        )
    )

    # Table
    df_table = df_table[[f'{filter_axis}','Quantity Ordered',
                                  '%Quantity Ordered',
                                  'Profit Margin',
                                  '%Profit Margin']]
    df_table.rename(columns={'Quantity Ordered':'Count',
                             '%Quantity Ordered':'Count%',
                             '%Profit Margin':'%Profit.M'}, inplace=True)
    columns = [{'name': col, 'id': col} for col in df_table.columns]
    data = df_table.to_dict('records')

    # Barchart
    barchart = px.bar(df_barchart_table, x=f'{filter_axis}', y='Revenue',
                        title=f'Revenue By: {filter_axis}',
                        color_discrete_sequence=['#100a61']
                        )

    # Update layout for better visualization
    barchart.update_layout(
        xaxis_title='Company',
        yaxis_title='Revenue',
        title_font=dict(color='white'),
        xaxis=dict(color='white'),
        yaxis=dict(tickformat=",.2s",color='white'),
        xaxis_showgrid=False, 
        yaxis_showgrid=False,
        plot_bgcolor='#040d15',
        paper_bgcolor='#040d15',
        margin=dict(l=10, r=10, b=10, t=60)  # Set the background color of the entire chart area
    )

    # Barchart Tkm
    df_barH = df_barchart_table.sort_values(by='Average Ticket', ascending=True)
    barchart_tkm = px.bar(
        df_barH,
        x='Average Ticket',
        y=f'{filter_axis}',
        orientation='h',
        color_discrete_sequence=['#100a61'],
        title=f'Average Ticket by {filter_axis}',
        custom_data=['%Quantity Ordered', '%Revenue', '%Profit Margin', '%Average Ticket'],  # Add percentage metrics to custom_data
    )

    # Update layout for better visualization
    barchart_tkm.update_layout(
        title_font=dict(color='white'),
        xaxis=dict(color='white'),
        yaxis=dict(tickformat=",.0f",color='white'),
        xaxis_showgrid=False, 
        yaxis_showgrid=False,
        plot_bgcolor='#040d15',
        paper_bgcolor='#040d15',
        margin=dict(l=10, r=10, b=10, t=60),
        hoverlabel=dict(bgcolor='#ffffff'),
        hovermode='closest',
    )

    # Update hover template
    barchart_tkm.update_traces(
        hovertemplate="<b>Average Ticket</b>: %{x}<br>" +
                    "<b>Company</b>: %{y}<br>" +
                    "<b>%Quantity Ordered</b>: %{customdata[0]:.2f}%<br>" +
                    "<b>%Revenue</b>: %{customdata[1]:.2f}%<br>" +
                    "<b>%Profit Margin</b>: %{customdata[2]:.2f}%<br>" +
                    "<b>%Average Ticket</b>: %{customdata[3]:.2f}%<extra></extra>"
    )

    # Create Lineplot
    lineplot_revenue = go.Figure()
    lineplot_revenue.add_trace(
        go.Scatter(
            x=df_lineplot['MonthYear'],
            y=df_lineplot['Revenue'],
            mode='lines+markers',
            line=dict(color='#0c6e4e'),
            marker=dict(color='#0c6e4e'),
            name='Monthly Revenue'
        )
    )

    # Update layout
    lineplot_revenue.update_layout(
        title='Monthly Revenue',
        title_font=dict(color='white'),
        xaxis_title='Month-Year', 
        yaxis_title='Revenue',
        yaxis=dict(tickformat=",.2s",color='white'),
        xaxis=dict(color='white'), 
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        plot_bgcolor='#060d13',
        paper_bgcolor='#060d13',
        margin=dict(l=10, r=10, b=10, t=60),
        hoverlabel=dict(bgcolor='#ffffff'),
        hovermode='closest',
        legend=dict(font=dict(color='white'))
    )
    # Add a trendline using linear regression
    z = np.polyfit(range(len(df_lineplot)), df_lineplot['Revenue'], 1)
    p = np.poly1d(z)

    lineplot_revenue.add_trace(go.Scatter(x=df_lineplot['MonthYear'], 
                                          y=p(range(len(df_lineplot))),
                                          mode='lines', 
                                          name='Trendline', 
                                          line=dict(color='red', dash='dash')))

    # Create Lineplot_growing up
    lineplot_growth = go.Figure()
    lineplot_growth.add_trace(
        go.Scatter(
            x=df_lineplot['MonthYear'],
            y=df_lineplot['CumulativeRevenue'],
            mode='lines+markers',
            name='CumulativeRevenue',
            line=dict(color='#0c6e4e'),
            marker=dict(color='#0c6e4e'),
            hovertext=df_lineplot['%MonthlyGrowth'],  # Add %MonthlyGrowth to hover text
        )
    )
    # Update layout
    lineplot_growth.update_layout(
        title='Cumulative Revenue and Monthly Growth Over Time',
        title_font=dict(color='white'),
        xaxis_title='Month-Year',
        yaxis_title='CumulativeRevenue',
        yaxis=dict(tickformat=",.2s",color='white'),  
        xaxis=dict(color='white'), 
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        plot_bgcolor='#060d13',
        paper_bgcolor='#060d13', 
        margin=dict(l=10, r=10, b=10, t=60),
        hoverlabel=dict(bgcolor='#ffffff'),
        hovermode='closest' 
    )

    return treemap, map_state, columns, data , barchart, barchart_tkm, lineplot_revenue,lineplot_growth
# Update Cards
def update_cards_content(filter_axis):
    df_grouped, df_table = etl_instance.etl_barchart_table(filter_axis)

    amt_sales = df_grouped['Quantity Ordered'].sum()
    revenue = df_grouped['Revenue'].sum()
    average_ticket = str(round(revenue / amt_sales,2))
    profit = df_grouped['Profit Margin'].sum()
    perc_profit = str(round(100 * profit / revenue,2)) + '%'

    # Generate content for each card
    card_1_content = "Amount Sales: {:,.0f}".format(float(amt_sales))
    card_2_content = "Revenue: ${:,.2f}".format(float(revenue))
    # Assuming average_ticket is a numeric value
    card_3_content = "Average Ticket: ${:,.2f}".format(float(average_ticket))
    card_4_content = "Gross Profit: ${:,.2f}".format(float(profit))
    card_5_content = f"% Profit: {perc_profit}"

    return card_1_content, card_2_content, card_3_content, card_4_content, card_5_content


    
