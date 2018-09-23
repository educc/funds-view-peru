import os
import json
import dash
import pandas
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

app = dash.Dash()

_DATA_PATH = "./data"
_FILE_FUNDS = "funds_list_ordered.csv"

def fund_list():
    df = pandas.read_csv(_FILE_FUNDS, sep=";")
    mylist = df.to_dict("records")
    return mylist

def load_data_fund(code: str):
    filename = os.path.join(_DATA_PATH, code + ".json")
    with open(filename, "r", encoding="utf-8") as myfile:
        jsondata = json.loads(myfile.read())
        for item in jsondata["quotes"]:
            item["date"] = dt.strptime(item["date"], "%d/%m/%Y")
        return pandas.DataFrame.from_dict(jsondata["quotes"])
    #end-with
    return None 
#end-def

app.layout = html.Div([
    html.H1('All Funds in Peru'),
    dcc.Dropdown(
        id='my-dropdown',
        options= fund_list(),
        value='0001-6107'
    ),
    dcc.Graph(id='my-graph')
])

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    df = load_data_fund(selected_dropdown_value)
    return {
        'data': [{
            'x': df.date,
            'y': df.value
        }]
    }



if __name__ == '__main__':
    app.run_server(port=8080, host="0.0.0.0", debug=True)
