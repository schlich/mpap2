import os, dash, json
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import pygsheets as pyg
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

client = pyg.authorize(service_account_env_var = 'GOOGLE_SHEETS_CREDS_JSON')

worksheet = client.open("cleaned_police_data").sheet1
rawdata = worksheet.get_all_values()
headers = rawdata.pop(0)
data = pd.DataFrame(rawdata, columns=headers)

race_counts = data['race of complainant'].value_counts()
officers = data['Officer Name'].unique()
display_data = data[['Officer Name','Date of Incident','Location of Incident','Nature of Complaint',"Complainant's Statement"]]
column_names = ['Date of Incident','Location of Incident','Nature of Complaint']

app.layout = html.Div([
    html.H2('St Louis Police Complaints'),
	html.H5('Search for/select an officer'),
	html.Datalist(id='officers', children = [html.Option(value=i) for i in officers]),
	dcc.Input(id='officer_input', list='officers'),
	html.Button('Search',id='submit'),
	html.Div([
		html.Div(
			dash_table.DataTable(
				id='complaints',
				columns=[{"name": i, "id": i, 'selectable': True} for i in column_names],
				data=pd.DataFrame().to_dict('records'),
				# hidden_columns=['Officer Name'],
				row_selectable='single',
				style_data={
					'whiteSpace': 'normal',
					'height': 'auto'
				},
			), className='six columns'
		),
		html.Div([
			html.H3("Complainant's Statement:"),
			html.P("Search for an officer and select a row to view the complainant's statement",id='statement')
		], className='six columns')
	], className='row', id='complaints_html', style= {'display': 'none'}),
	dcc.Graph(
		figure=go.Figure(
			data=go.Pie(
				labels=race_counts.index.tolist(),
				values=race_counts.values.tolist(),
				textinfo='label+value'
			)
		)
	)

])

@app.callback(
	[dash.dependencies.Output('complaints', 'data'),
	dash.dependencies.Output('complaints_html','style')],
	[dash.dependencies.Input('submit', 'n_clicks')],
    [dash.dependencies.State('officer_input', 'value')])
def update_data(n_clicks,officer):
	if not n_clicks:
		raise PreventUpdate
	else:
		complaints = display_data[display_data['Officer Name']==officer].to_dict('records')
		return complaints, {'display':'block'}

@app.callback(
	dash.dependencies.Output('statement','children'),
     [dash.dependencies.Input('complaints', "derived_virtual_selected_rows")],
	 [dash.dependencies.State('complaints', "derived_virtual_data")],
)
def get_statement(derived_virtual_selected_rows, row):
	print(derived_virtual_selected_rows)
	if not derived_virtual_selected_rows:
		statement = "Select a row to view the complainant's statement"
	else:
		selected_row =  pd.DataFrame(row)
		statement = selected_row["Complainant's Statement"]

	return statement

if __name__ == '__main__':
    app.run_server(debug=True)