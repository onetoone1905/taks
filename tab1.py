# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 10:31:21 2020

@author: TM5A5F7N
"""

import app

import datetime
import time

from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd

#### Graphs ####
import plotly.express as px
import plotly.graph_objects as go
import base64


def serve_layout():
    try :
        df
    except NameError:
        print("well, it WASN'T defined after all!")
    else:
        print("sure, it was defined.")
    return html.Div([html.Div([
        html.Div([html.H6("Welcome, first upload your training dataset file", style=dict(size=10))], style={'width': '80%',
            'max-width': '90vw','margin':'0 auto 0'}),html.Br(),
    html.Div([
    html.Div([dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select your training file')
        ]),
        style={
            'width': '80%',
            'max-width': '90vw',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin':'0 auto 0', 
            'color'  : 'grey'
        },
        # Allow multiple files to be uploaded
        multiple=True
    )], className = "twelve columns"), #six col if two uploads
    ], className='row'),
    html.P(),
    html.Div(id='output-data-upload'),html.Div(id='hidden-div-test', style={'display':'none'}),
],style={
            'width': '80%',
            'max-width': '90vw',
            'margin' : '0 auto 0'})
,html.Div([
        # Create element to hide/show, in this case an 'Input Component'
    ], style= {'display': 'block', 'margin-left' : 110} # <-- This is the line that will be changed by the dropdown callback
    )])
    
    