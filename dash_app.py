import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

dark_mode = [dbc.themes.DARKLY] # putting in dark mode cause we cool like that 
app = dash.Dash(__name__, title='Data Dashboard', external_stylesheets=[dark_mode])

df = pd.read_csv('dummy_data.csv') # read in CSV -> how does this change w the database? sus 

app.layout = html.Div([
    html.Div([
        html.Label('Select Feature:', style={'color': 'white'}),
        dcc.Dropdown(
            id='feature-dropdown',
            options=[
                {'label': 'Throughput', 'value': 'Throughput'},
                {'label': 'Latency', 'value': 'Latency'},
                {'label': 'Video Resolution', 'value': 'Video Resolution'},
                {'label': 'Age of Device', 'value': 'Age of Device'},
                {'label': 'Resolution Switches', 'value': 'Resolution Switches'}
            ],
            multi=True
        )
    ], style={'padding': '10px'}),
    html.Div([
        html.Div([
            html.Label('Select State:', style={'font-size': '18px', 'color': 'white'}),
            dcc.RadioItems(
                id='state-radio',
                options=[{'label': state, 'value': state} for state in df['state'].unique()],
                value='California'
            )
        ], style={'padding': '10px', 'color': 'white'}),
        html.Div([
            html.Label('Select Service Provider:', style={'font-size': '18px', 'color': 'white'}),
            dcc.RadioItems(
                id='provider-radio',
                options=[{'label': provider, 'value': provider} for provider in ['A', 'B', 'C', 'D', 'E']],
                value='A'
            )
        ], style={'padding': '10px', 'color': 'white'}),
        html.Div([
            html.Label('Select Aggregate Type:', style={'font-size': '18px', 'color': 'white'}),
            dcc.RadioItems(
                id='aggregate-radio',
                options=[
                    {'label': 'Median', 'value': 'median'},
                    {'label': 'Average', 'value': 'average'},
                    {'label': '90th Percentile', 'value': '90th'},
                    {'label': '10th Percentile', 'value': '10th'}
                ],
                value='average'
            )
        ], style={'padding': '10px', 'color': 'white'}),
        html.Div([
            html.Label('Select Time Frame:', style={'font-size': '18px', 'color': 'white'}),
            dcc.RadioItems(
                id='timeframe-radio',
                options=[
                    {'label': 'Monthly', 'value': 'monthly'},
                    {'label': 'Weekly', 'value': 'weekly'},
                    {'label': 'Daily', 'value': 'daily'}
                ],
                value='monthly'
            )
        ], style={'padding': '10px', 'color': 'white'})
    ], style={'float': 'right', 'width': '20%', 'padding': '10px'}),
    html.Div([
        dcc.Graph(id='line-graph')
    ], style={'marginRight': '25%'}),
        html.Div([
            html.Div([
                html.Div([
                    html.Label('State Selection', style={'font-size': '18px', 'color': 'white'}),
                    dcc.Dropdown(
                        id='state-dropdown',  # every unique div needs a unique id -> dont forget 
                        options=[{'label': state, 'value': state} for state in df['state'].unique()], # takes all unique states and puts them in the drop down
                        value='Cali',
                        clearable=False # this implies something is always selected, default val = Cali 
                    )
                ], style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                    html.Label('Service Provider Selection', style={'font-size': '18px', 'color': 'white'}),
                    dcc.Dropdown(
                        id='provider-dropdown',
                        options=[{'label': provider, 'value': provider} for provider in df['service provider'].unique()],
                        value='Provider A',
                        clearable=False
                    )
                ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'})
            ], style={'backgroundColor': 'rgb(17, 17, 17)', 'padding': '10px 5px'}),

            html.Div([
                dcc.Graph(id='pie-chart')
            ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
            html.Div([
                dcc.Graph(id='scatter-plot')
            ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        ], style={'backgroundColor': 'rgb(0, 0, 0)'})
], style={'backgroundColor': 'rgb(17, 17, 17)', 'padding': '10px 5px'})


@app.callback(
    dash.dependencies.Output('line-graph', 'figure'),
    [
        dash.dependencies.Input('state-radio', 'value'),
        dash.dependencies.Input('provider-radio', 'value'),
        dash.dependencies.Input('aggregate-radio', 'value'),
        dash.dependencies.Input('timeframe-radio', 'value'),
        dash.dependencies.Input('feature-dropdown', 'value')
    ]
)

def update_graph(state, provider, aggregate, timeframe, selected_features):
    dff = df[(df['state'] == state) & (df['service provider'] == provider)]
    
    if timeframe == 'monthly':
        dff = dff.set_index('date').resample('M').mean().reset_index()
    elif timeframe == 'weekly':
        dff = dff.set_index('date').resample('W').mean().reset_index()
    else:
        dff = dff.set_index('date').resample('D').mean().reset_index()

    if aggregate == 'median':
        dff = dff.median()
    elif aggregate == '90th':
        dff = dff.quantile(0.90)
    elif aggregate == '10th':
        dff = dff.quantile(0.10)
    else:
        dff = dff.mean()

    if not selected_features:
        selected_features = ['throughput', 'latency', 'video resolution', 'age of device', 'resolution switches']

    data = []
    for feature in selected_features:
        fig = px.line(dff, x='date', y=feature, title=f'Network Performance - {feature}')
        fig.update_layout(
            paper_bgcolor='rgb(17, 17, 17)',
            plot_bgcolor='rgb(17, 17, 17)',
            font=dict(color='white'),
            xaxis=dict(title='Date', color='white'),
            yaxis=dict(title='Value', color='white'),
            title=dict(font=dict(color='white'))
        )
        data.append(fig)

    # Create a combined figure with subplots if multiple features are selected
    if len(data) > 1:
        fig = make_subplots(rows=len(data), cols=1, shared_xaxes=True)
        for i, single_fig in enumerate(data):
            for trace in single_fig['data']:
                fig.add_trace(trace, row=i+1, col=1)
        fig.update_layout(
            height=400*len(data),
            paper_bgcolor='rgb(17, 17, 17)',
            plot_bgcolor='rgb(17, 17, 17)',
            font=dict(color='white'),
            title='Network Performance'
        )
    else:
        fig = data[0]

    return fig


@app.callback(
    dash.dependencies.Output('pie-chart', 'figure'),
    [
        dash.dependencies.Input('state-dropdown', 'value'),
        dash.dependencies.Input('provider-dropdown', 'value')
    ]
)
def update_pie_chart(selected_state, selected_provider):
    filtered_df = df[(df['state'] == selected_state) & (df['service provider'] == selected_provider)]
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


# Callback for updating the scatter plot based on state and service provider
@app.callback(
    dash.dependencies.Output ('scatter-plot', 'figure'),
    [
        dash.dependencies.Input('state-dropdown', 'value'),
        dash.dependencies.Input('provider-dropdown', 'value')
    ]
)
def update_scatter_plot(selected_state, selected_provider):
    filtered_df = df[(df['state'] == selected_state) & (df['service provider'] == selected_provider)]
    fig = px.scatter(
        filtered_df,
        x='throughput', # defines x axis
        y='latency', # defines y axis
        color='video resolution', # the colour of the point is decides using the video resolution value 
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


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=5000)