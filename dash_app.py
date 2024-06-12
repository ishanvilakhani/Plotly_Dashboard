import dash
import numpy as np 
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import pandas as pd

dark_mode = [dbc.themes.DARKLY] # putting in dark mode cause we cool like that 
app = dash.Dash(__name__, title='Data Dashboard', external_stylesheets=[dark_mode])

df = pd.read_csv('dummy_data.csv') # read in CSV -> how does this change w the database? sus 

# break down the page into HTML DIVS
app.layout = html.Div([
    html.Div([
        html.Label('Select Aggregation Method', style={'font-size': '18px', 'color': 'white'}),
        dcc.RadioItems(
            id='aggregation-method',
            options=[
                {'label': 'Sum', 'value': 'sum'},
                {'label': 'Average', 'value': 'mean'},
                {'label': 'Median', 'value': 'median'},
                {'label': '90th Percentile', 'value': '90th'},
                {'label': '10th Percentile', 'value': '10th'}
            ],
            value='mean',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'}
        ),
    ], style={'width': '100%', 'padding': '10px 5px'}),

    html.Div([
        html.Label('Select Time Frame', style={'font-size': '18px', 'color': 'white'}),
        dcc.RadioItems(
            id='time-frame',
            options=[
                {'label': 'Monthly', 'value': 'monthly'},
                {'label': 'Weekly', 'value': 'weekly'},
                {'label': 'Daily', 'value': 'daily'}
            ],
            value='daily',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'}
        ),
    ], style={'width': '100%', 'padding': '10px 5px'}),

    html.Div([
        html.Label('Select Service Provider and State', style={'font-size': '18px', 'color': 'white'}),
        dcc.Dropdown(
            id='provider-dropdown',
            options=[{'label': provider, 'value': provider} for provider in df['service provider'].unique()],
            value=None,
            placeholder="Select Provider",
            clearable=True,
            style={'margin-bottom': '10px'}
        ),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': state, 'value': state} for state in df['state'].unique()],
            value=None,
            placeholder="Select State",
            clearable=True,
            style={'margin-bottom': '10px'}
        )
    ], style={'width': '100%', 'padding': '10px 5px'}),

    html.Div([
        dcc.Graph(id='scatter-plot')
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dcc.Graph(id='pie-chart')
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
], style={'backgroundColor': 'rgb(17, 17, 17)'})


@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    [dash.dependencies.Input('provider-dropdown', 'value'),
     dash.dependencies.Input('state-dropdown', 'value'),
     dash.dependencies.Input('aggregation-method', 'value'),
     dash.dependencies.Input('time-frame', 'value')]
)
def update_scatter_plot(selected_provider, selected_state, aggregation_method, time_frame):
    filtered_df = df.copy()

    if selected_provider:
        filtered_df = filtered_df[filtered_df['service provider'] == selected_provider]
    if selected_state:
        filtered_df = filtered_df[filtered_df['state'] == selected_state]

    if aggregation_method == '90th':
        aggregation_func = lambda x: np.percentile(x, 90)
    elif aggregation_method == '10th':
        aggregation_func = lambda x: np.percentile(x, 10)
    else:
        aggregation_func = aggregation_method

    if time_frame == 'monthly':
        filtered_df['date'] = pd.to_datetime(filtered_df['date'])
        filtered_df = filtered_df.resample('M', on='date').agg(aggregation_func)
    elif time_frame == 'weekly':
        filtered_df['date'] = pd.to_datetime(filtered_df['date'])
        filtered_df = filtered_df.resample('W', on='date').agg(aggregation_func)
    else:
        filtered_df = filtered_df.groupby('date').agg(aggregation_func).reset_index()

    fig = px.scatter(
        filtered_df,
        x='throughput',
        y='latency',
        color='video resolution',
        size='age of device',
        hover_data=['resolution switches'],
        title=f'Scatter plot for {selected_provider} in {selected_state}'
    )
    fig.update_layout(
        paper_bgcolor='rgb(17, 17, 17)',
        plot_bgcolor='rgb(17, 17, 17)',
        font=dict(color='white')
    )
    return fig


@app.callback(
    dash.dependencies.Output('pie-chart', 'figure'),
    [dash.dependencies.Input('provider-dropdown', 'value'),
     dash.dependencies.Input('state-dropdown', 'value')]
)
def update_pie_chart(selected_provider, selected_state):
    filtered_df = df.copy()

    if selected_provider:
        filtered_df = filtered_df[filtered_df['service provider'] == selected_provider]
    if selected_state:
        filtered_df = filtered_df[filtered_df['state'] == selected_state]

    age_counts = filtered_df['age of device'].value_counts().reset_index()
    age_counts.columns = ['age of device', 'count']
    
    fig = px.pie(
        age_counts, 
        names='age of device', 
        values='count',
        title=f'Distribution of Device Ages for {selected_provider} in {selected_state}',
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig.update_layout(
        paper_bgcolor='rgb(17, 17, 17)',
        plot_bgcolor='rgb(17, 17, 17)',
        font=dict(color='white')
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=5000)