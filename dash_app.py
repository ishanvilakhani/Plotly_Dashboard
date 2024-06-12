# import dash
# import pandas as pd
# from dash import dcc
# from dash import dbc
# from dash import html
# from dash import dash_table

# # just incase i forget what div or any otheer tool does
# # help(html.Div) 
# # help(dcc.Div) 

# external_stylesheets = [dbc.themes.DARKLY]
# app = dash.Dash()
# df = pd.read_csv('dummy_data.csv')

# output_data = ['hi']
# app.layout = html.Div([
#     html.H1(
#             children = 'YOUR DATA DASHBOARD', 
#             style = { 
#                     'textAlign' : 'center', 
#                     'color' : '#780276'
#                     }
#             ), 
#     html.Div(output_data), 

#     dcc.Graph(
#         id = 'sample_graph',
#         figure = { 
#             'data' : [{'x': [5,6,7], 'y':[12,15,187], 'type':'bar', 'name':'SF'}, {'x': [5,6,7], 'y':[12,15,187], 'type':'bar', 'name':'SF2'}], 
#             'layout' : {
#                 'plot_bgcolor' : '#780276', 
#                 'paper_bgcolor' : '#000000',
#                 'title' : 'BASIC BAR CHART',
#                 'font': {
#                     'color' : '#FFFFFF'
#                 }
#             }
#         }
#     )
# ])

# # connecting and starting the server 
# if __name__ == '__main__':
#     app.run_server(port =5000)




# # output_data = ['hi']
# # app.layout = html.Div([
# #     html.H1(
# #             children = 'YOUR DATA DASHBOARD', 
# #             style = { 
# #                     'textAlign' : 'center', 
# #                     'color' : '#780276'
# #                     }
# #             ), 
# #     html.Div(output_data), 

# #     dcc.Graph(
# #         id = 'sample_graph',
# #         figure = { 
# #             'data' : [{'x': [5,6,7], 'y':[12,15,187], 'type':'bar', 'name':'SF'}, {'x': [5,6,7], 'y':[12,15,187], 'type':'bar', 'name':'SF2'}], 
# #             'layout' : {
# #                 'plot_bgcolor' : '#780276', 
# #                 'paper_bgcolor' : '#000000',
# #                 'title' : 'BASIC BAR CHART',
# #                 'font': {
# #                     'color' : '#FFFFFF'
# #                 }
# #             }
# #         }
# #     )
# # ])




# import dash
# import pandas as pd
# from dash import dcc
# from dash import dbc
# from dash import html
# from dash import dash_table

# # just incase I forget what div or any other tool does
# # help(html.Div) 
# # help(dcc.Div) 

# external_stylesheets = [dbc.themes.DARKLY]
# app = dash.Dash()
# df = pd.read_csv('dummy_data.csv')

# html.Div ([ # big div that includes the whole page 

# # figure out how to divide the page and make the divs accordingly
# # every interactive component needs a unqiue id 


# ])

# # if theres a call bak what it means is if trheres a change in thi function -> use these values and update and clal this function 
# # call backs usually have 2 things -> outputs and inputs 


import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import pandas as pd

external_stylesheets = [dbc.themes.DARKLY]

# read data and store as df 
data = pd.read_csv('dummy_data.csv')
df = pd.DataFrame(data)

# make it dark theme cause thats cooler 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define the layout of the app
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Bar Chart Example", className="text-center mt-4")
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='bar-chart',
                    figure=px.bar(df, x='service provider', y='age of device', title='Sample Bar Chart')
                )
            )
        )
    ],
    fluid=True
)

# connecting and starting the server 
if __name__ == '__main__':
    app.run_server(port =5000)

