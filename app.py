import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

data = pd.read_csv('cleaned_police_data.csv')

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