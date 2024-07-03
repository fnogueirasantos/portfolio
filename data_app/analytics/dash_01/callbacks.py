import plotly.express as px
import plotly.graph_objects as go
from .etl import Etl
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Assuming etl.Etl is your class
etl_instance = Etl()


def update_barcharts(selected_option):
    # Callback first barchat
    df_count = etl_instance.etl_barchart(selected_option)
    fig_count = px.bar(
        df_count,
        x=selected_option,
        y='id',
        color='NPSGroup',
        title=f'Bar Chart by {selected_option} with Count and Percentage in Legend',
        labels={'id': 'Count', 'Text': 'Percentage'},
        text='Text',
        color_discrete_map = {'Dissatisfied': '#FF3434', 'Neutral': '#FFFF99', 'Satisfied': 'green'}
    ).update_layout(
        title=dict(
            text=f'Bar Chart by {selected_option} with Count and Percentage',
            font=dict(size=14, color='black')
        ),
        xaxis=dict(
            title=dict(
                text=selected_option
            ),
            tickfont=dict(size=14, color='black'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(
                text='Frequency',
                font=dict(size=16, color='black')
            ),
            tickfont=dict(size=14, color='black'),
            showgrid=False
        ),
        legend=dict(
            orientation='h',
            x=0.5,
            y=1.1,
            title=' '
        ),
        margin=dict(l=10, r=10, b=10, t=60),
        paper_bgcolor='lightgray',
        plot_bgcolor='lightgray',
        bargap=0.1,
        uniformtext=dict(mode='hide', minsize=10),
    )

    # Callback feature barchat
    feature_importance_df = etl_instance.etl_machine_learning()
    fig_feature =px.bar(
        feature_importance_df,
        x='Feature',
        y='Importance',
        color_discrete_sequence=['#210011'],
        labels={'Feature': 'Feature Importance'}
    ).update_layout(
        title=dict(
            text=f'Feature Importance Static Chart - Top 10 importance of features in the decision tree model',
            font=dict(size=14, color='black')
        ),
        xaxis=dict(
            title=dict(
                text='Features'
            ),
            tickfont=dict(size=14, color='black'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(
                text='Ranking of the Model',
                font=dict(size=14, color='black')
            ),
            tickfont=dict(size=14, color='black'),
            showgrid=False
        ),
        paper_bgcolor='lightgray',
        plot_bgcolor='lightgray',
        margin=dict(l=10, r=10, b=10, t=60),
        bargap=0.1,
        uniformtext=dict(mode='hide', minsize=10),
    )

    # Callback filters for secondDropdown
    df_filter = etl_instance.etl_histogram(selected_option)
    unique_values = list(df_filter[f'{selected_option}'].unique())
    unique_values.append('All')
    # Sort unique values alphabetically
    sorted_values = sorted(unique_values)
    options = options = [{'label': value, 'value': value} for value in sorted_values]
    second_filter = 'All' if options else None

    return fig_count, fig_feature, options, second_filter

def update_histogram(selected_option, sencond_filter):
    # Callback Histogram
    if sencond_filter == "All":
        df_histogram = etl_instance.etl_histogram(selected_option)
    else:
        df_histogram = etl_instance.etl_histogram(selected_option)
        df_histogram = df_histogram[df_histogram[selected_option] == sencond_filter]
    fig_histogram = px.histogram(
        df_histogram,
        x='Nps',
        nbins=10,
        histnorm='percent',
        color_discrete_sequence=['#210011'] 
    ).update_layout(
        title=dict(
            text=f'Histogram of the Variable {selected_option} with filter per: {sencond_filter}',
            font=dict(size=14, color='black')
        ),
        xaxis=dict(
            title=dict(
                text='Evaluation'
            ),
            tickfont=dict(size=16, color='black'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(
                text='Frequency %',
                font=dict(size=16, color='black')
            ),
            tickfont=dict(size=16, color='black'),
            showgrid=False
        ),
        paper_bgcolor='lightgray',
        plot_bgcolor='lightgray',
        margin=dict(l=10, r=10, b=10, t=60),
    )

    #calback Barchart Services
    if sencond_filter == "All":
        df_filtered = etl_instance.dataset
        df_filtered = etl_instance.etl_barcahart_services(df_filtered)
    else:
        df_filtered = etl_instance.dataset
        df_filtered = df_filtered[df_filtered[selected_option] == sencond_filter]
        df_filtered = etl_instance.etl_barcahart_services(df_filtered)

    general_target = 7
    max_target = 10
    fig_barchart_services = px.bar(df_filtered, x='Feature', y='Mean', color='ModelGroup',
                labels={'Mean': 'Mean Value'}, color_discrete_map = {'Low': '#FF3434', 'Neutral': '#FFFF99', 'High': 'green'}
    )

    fig_barchart_services.add_trace(go.Scatter(x=df_filtered['Feature'], y=[general_target] * len(df_filtered),
                            mode='lines', name='Target', line=dict(color='black', dash='dash')))
    fig_barchart_services.add_trace(go.Scatter(x=df_filtered['Feature'], y=[max_target] * len(df_filtered),
                            mode='lines', name='', line=dict(color='lightgray', dash='dash')))
    fig_barchart_services.update_layout(
        xaxis=dict(title='Feature'),
        yaxis=dict(title='Mean Value'),
        legend=dict(title='ModelGroup'),
        barmode='group',
    ).update_layout(
        title=dict(
            text=f'Mean values by Service Evaluation with filter per: {sencond_filter}',
            font=dict(size=16, color='black')
        ),
        xaxis=dict(
            title=dict(
                text='Features'
            ),
            tickfont=dict(size=14, color='black'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(
                text='Mean Value',
                font=dict(size=14, color='black')
            ),
            tickfont=dict(size=14, color='black'),
            showgrid=False
        ),
        paper_bgcolor='lightgray',
        plot_bgcolor='lightgray',
        margin=dict(l=10, r=10, b=10, t=60),
    )
    return fig_histogram, fig_barchart_services


def update_cards(selected_option, sencond_filter):
    # Assuming etl_instance.dataset is your DataFrame
    df_filtered = etl_instance.dataset.copy()

    if sencond_filter != "All":
        df_filtered = df_filtered[df_filtered[selected_option] == sencond_filter]

    # Number of Searches
    searches = len(df_filtered)
    
    # Mean Evaluation
    mean_evaluation = round(df_filtered['Nps'].mean(), 2)

    # Count and percentage for each NPSGroup
    evaluation_groups = ['Satisfied', 'Neutral', 'Dissatisfied']
    card_content = {}

    for nps_group in evaluation_groups:
        count = len(df_filtered[df_filtered['NPSGroup'] == nps_group])
        percentage = round(count / searches * 100, 2)
        card_content[nps_group] = f"{nps_group}: {count} | {percentage}%"

    # Generate content for each card
    card_1_content = f"Number of Searches: {searches}"
    card_2_content = f"Mean Evaluation: {mean_evaluation}"
    card_3_content = card_content.get('Satisfied', 'Satisfied: 0 | 0%')
    card_4_content = card_content.get('Neutral', 'Neutral: 0 | 0%')
    card_5_content = card_content.get('Dissatisfied', 'Dissatisfied: 0 | 0%')

    return card_1_content, card_2_content, card_3_content, card_4_content, card_5_content


