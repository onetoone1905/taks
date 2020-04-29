import io
import datetime
import pandas as pd
import time 
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

import dash_bootstrap_components as dbc

import dash_daq as daq

import tab1
import base64

from pathlib import Path


#server = app.server
    


#### App color ####
background_color= '#1e2130' #'#1e2130'
background_color3='rgba(0, 0, 0, 0.7)' #'rgba(0, 0, 0, 0)'
background_color2='rgba(0, 0, 0, 0)' #'rgba(0, 0, 0, 0)'
police_color='white'
police_tab_selected='#0080ff'#'#15b0f6'

table_as_list=True
### Definition des tabs
tabs_styles = {
    'height': '44px'
}
tab_height = '5vh'
tab_style={'padding': '0',
           'line-height': tab_height,
           'color' : police_color,
           'font-family':'Roboto',
           #'fontWeight': 'bold',
           'font-size' : 17} #3E6C96
selected_style={'padding': '0',
                'line-height': tab_height,
                #'fontWeight': 'bold',
                'font-size' : 20,
                'font-family':'Roboto',
                'color' : police_tab_selected,
                'backgroundColor' : background_color
                }

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
app.config.suppress_callback_exceptions = True

app.layout=html.Div([
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', style={'height' : tab_height,'padding-top': '57px'}, children=[
        dcc.Tab(label='Task', value='tab-1', style=tab_style, selected_style=selected_style),
        

    ], colors={
        "border": "light grey",
        "primary": police_tab_selected #"#15b0f6"#"#0096fe"
        ,"background": "dark grey" #"#e0e0e0"
    }),
    html.Div(id='tabs-content-props')
]#style={'backgroundColor' : '#434c6c'}
)
    

@app.callback(Output('tabs-content-props', 'children'),
              [Input('tabs-styled-with-props', 'value')])
def render_content(tab):
    #time.sleep(0.5)
    if tab == 'tab-1':
        #print("Session ID : ", session_id)
        return tab1.serve_layout()
    
def parse_contents(contents, filename, date):
    global session_id
    session_id=hash(time.time())
    global df
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    time.sleep(0.5)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            out_df=df.to_csv(path_or_buf='df_'+str(session_id)+'.csv')
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    time.sleep(10)
    return html.Div([
#        html.H5(filename),
#        html.H6(datetime.datetime.fromtimestamp(date)),
        html.Div([dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_header={"fontWeight": "bold", "color": police_color, "font_size" : 15},
            style_as_list_view=table_as_list,
            fill_width=True,
                         style_cell={
                "backgroundColor": background_color,
                "fontFamily": "sans-serif",
                "padding": "0 2rem",
                "color": police_color,
                "border": "none",
                "font_size" : 12
                        },
                       css=[
                {"selector": "tr:hover td", "rule": "color: #91dfd2 !important;"},
                {"selector": "td", "rule": "border: None !important;"},
                {
                    "selector": ".dash-cell.focused",
                    "rule": "background-color: %s !important;" %background_color,
                },
                {"selector": "table", "rule": "--accent: %s;" %background_color},
                {"selector": "tr", "rule": "background-color: transparent"},
            ],
            page_action="native",
            page_current= 0,
            page_size= 5,
            style_table={'minWidth': '100%', 'overflowX': 'scroll'}
        )],style={'width': '100%' , 'max-width': '90vw', 'margin':'0 auto 0'}),
    html.Div(id='dd-output-container'), 
        ],  style={
            'width': '80%',
            'max-width': '90vw',
            'margin' : '0 auto 0'})
            
            
@app.callback([Output('output-data-upload', 'children'),
              Output(component_id='element-to-hide', component_property='style')],
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return (children, {'display': 'none'})
    


if __name__ == '__main__':
    app.run_server(debug=False, port=8090)
    for p in Path(".").glob("df_"+str(session_id)+".csv"):
        p.unlink()
