import dash
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
        html.Div([
            html.Label('State Selection', style={'font-size': '18px', 'color': 'white'}),
            dcc.Dropdown(
                id='state-dropdown',  # every uniqu div needs a unique id -> dont forget 
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



@app.callback(
    dash.dependencies.Output('pie-chart', 'figure'),
    [dash.dependencies.Input('state-dropdown', 'value'),
     dash.dependencies.Input('provider-dropdown', 'value')]
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