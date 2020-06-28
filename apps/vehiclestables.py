from __future__ import print_function
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from app import app
import dash_core_components as dcc



fleet_data = pd.read_csv('cleaned-data-for-fleet-dna_v3.csv')
dfnames = pd.read_csv('names/names.csv')
#rounded data
fleet_data_rounded = fleet_data.round(decimals=2)


df_vehicle = fleet_data[['vid', 'vocation', 'vehicel_type', 'drivetrain_type','pid']].copy()
df_vehicle_class = fleet_data[['vehicle_class','vid', 'fuel_type', 'vocation','vehicel_type']].copy()

df_driver = fleet_data[['pid','vid', 'vehicel_type']].copy(),
df_driver_all = pd.merge(fleet_data, dfnames, how='left', on='pid')


available_vehicleclass = fleet_data_rounded['vehicle_class'].unique()

df_group_vehicle_class = fleet_data.groupby(["vehicle_class"], as_index=False)["vid"].count()
df_group_vehicle_class.columns = (["vehicle_class", "anzahl"])

layout = html.Div(children=[
    html.H1(children='Vehicles Tables'),

    html.Div(children='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut '
                      'labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco '
                      'laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in '
                      'voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat '
                      'non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'),
html.P(
html.Div(
        dash_table.DataTable(
            id ='table-sorting-filtering',
            columns=[{'name': i, 'id': i} for i in df_vehicle.loc[:]],
            data=df_vehicle.to_dict('records'),
            editable=True,

            row_selectable='multi',
            row_deletable=True,
            selected_rows=[],
            page_action='native',
            page_current=0,
            page_size=10,

            filter_action='native',
            filter_query='',

            sort_action='custom',
            sort_mode='multi',
            sort_by=[],
            style_table={'overflowX': 'scroll'},

            style_cell={'textAlign': 'left'},
            style_cell_conditional=[

            ]
        ),
),
    ),
html.P(
html.Div(
        dash_table.DataTable(
            id='table-sorting-filtering',
            columns=[{'name': i, 'id': i} for i in df_group_vehicle_class.loc[:]],
            data=df_group_vehicle_class.to_dict('records'),
            editable=True,

            row_selectable='multi',
            row_deletable=True,
            selected_rows=[],
            page_action='native',
            page_current=0,
            page_size=10,

            filter_action='native',
            filter_query='',

            sort_action='custom',
            sort_mode='multi',
            sort_by=[],
            style_table={'overflowX': 'scroll'},

            style_cell={'textAlign': 'left'},
            style_cell_conditional=[

            ]
        ),
),
    ),
html.P(
html.Div(
        dash_table.DataTable(
            id='table-sorting-filtering',
            columns=[{'name': i, 'id': i} for i in df_driver_all.loc[:]],
            data=df_driver_all.to_dict('records'),
            editable=True,

            row_selectable='multi',
            row_deletable=True,
            selected_rows=[],
            page_action='native',
            page_current=0,
            page_size=10,

            filter_action='native',
            filter_query='',

            sort_action='custom',
            sort_mode='multi',
            sort_by=[],
            style_table={'overflowX': 'scroll'},

            style_cell={'textAlign': 'left'},
            style_cell_conditional=[

            ]
        ),
    ),
),
    ])


