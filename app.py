import os
import dash
import gspread
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from apiclient.discovery import build
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials/quickstart-1569111830589-99d9dd4fa4d5.json', scope)
gc = gspread.authorize(credentials)
worksheet = gc.open("cleaned_police_data").sheet1
rawdata = worksheet.get_all_values()
headers = rawdata.pop(0)
data = pd.DataFrame(rawdata, columns=headers)

race_counts = data['race of complainant'].value_counts()

app.layout = html.Div([
    html.H2('St Louis Police Complaints'),
    dcc.Graph(
		figure=go.Figure(
			data=go.Pie(
				labels=race_counts.index.tolist(),
				values=race_counts.values.tolist(),
				textinfo='label+value'
			)
		)
    ),
    html.Div(id='display-value')
])

# @app.callback(dash.dependencies.Output('display-value', 'children'),
#               [dash.dependencies.Input('dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)