import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import pandas as pd

dark_mode = [dbc.themes.DARKLY]
app = dash.Dash(__name__, title='Data Dashboard', external_stylesheets=[dark_mode])

df = pd.read_csv('dummy_data.csv')

app.layout = html.Div([
    html.Div([

        html.Div([
            
            html.Div([
                html.Label('Model selection'),], style={'font-size': '18px'}),
            
            dcc.Dropdown(
                id='crossfilter-model',
                options=[ 
            		{'label' : 'Principal Component Analysis', 'value' : 'PCA'}, 
					{'label' : 'Uniform Manifold Appriximation and Projection', 'value' : 'UMAP'},
					{'label' : 'Autoencoder', 'value' : 'AE'},
					{'label' : 'Variational Autoencoder', 'value' : 'VAE'}
                ],
                value = 'PCA', 
				clearable = False # to make sure atleast one thingis always selected and doesnt get cleared
          
            )], style={'width': '49%', 'display': 'inline-block'}
        ),

        html.Div([
            
            html.Div([
                html.Label('Feature selection'),], style={'font-size': '18px', 'width': '40%', 'display': 'inline-block'}),
            
            html.Div([
                    dcc.RadioItems(
                        id='gradient-scheme',
                        options=[
                            {'label': 'Orange to Red', 'value': 'OrRd'}, 
                            {'label': 'Viridis', 'value': 'Viridis'}, 
                            {'label': 'Plasma', 'value': 'Plasma'}, 
                        ],
                        value='Plasma',
                        labelStyle={'float': 'right', 'display': 'inline-block', 'margin-right': 10, 'color': 'white'}
                    ),
                ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'}),
            
            dcc.Dropdown(
                id='crossfilter-feature',
                options= [{'label' : i, 'value' : i} for i in df['state'].unique()], 
                value='None',
                clearable=False
            )], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}
        
        )], style={'backgroundColor': 'rgb(17, 17, 17)', 'padding': '10px 5px'}
    ),

    html.Div([

        dcc.Graph(
            id= 'SCATTER-PLOT',
            hoverData={'points': [{'customdata': 0}]}
        )

    ], style={'width': '100%', 'height':'90%', 'display': 'inline-block', 'padding': '0 20'}),
    
    html.Div([
        dcc.Graph(id='point-plot'),
    ], style={'display': 'inline-block', 'width': '100%'}),

    ], style={'backgroundColor': 'rgb(17, 17, 17)'},
)


@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'), 
    [
        dash.dependencies.Input('crossfilter-feature', 'value'),
        dash.dependencies.Input('crossfilter-feature', 'value'),
        dash.dependencies.Input('gradient-scheme', 'value'),
    ]
)
def update_graph(feature, model, gradient):
    fig = px.scatter (
        df, 
        x = df[f'{model.lower()}_x'],
        y = df[f'{model.lower()}_y'],
        opacity = 0.8, 
        template = 'plotly_dark',
        colour_coninout_scare = gradient
    ) 


def create_point_plot(df, title):
    return None


@app.callback(
    ###
)
def update_point_plot(hoverData):
    return None

# connecting and starting the server 
if __name__ == '__main__':
    app.run_server(port =5000)

