
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd


# Datasets


fleet_data = pd.read_csv('cleaned-data-for-fleet-dna_v3.csv')
fleet_data.drop_duplicates(keep=False,inplace=True)

dfnames = pd.read_csv('names/names.csv')
#rounded data
fleet_data_rounded = fleet_data.round(decimals=2)


df_vehicle = fleet_data[['vid','vehicle_class', 'vocation', 'vehicel_type', 'drivetrain_type','pid']].copy()
df_vehicle = df_vehicle.drop_duplicates(subset=None, keep='first', inplace=False)

df_vehicle_class = fleet_data[['vehicle_class','vid', 'fuel_type', 'vocation','vehicel_type']].copy()
df_vehicle_class = df_vehicle_class.drop_duplicates(subset=None, keep='first', inplace=False)


df_group_vehicle_class = fleet_data.groupby(["vehicle_class"], as_index=False)["vid"].count()
df_group_vehicle_class.columns = (["Klasse", "anzahl"])
df_group_vehicle_class = df_group_vehicle_class.drop_duplicates(subset=None, keep='first', inplace=False)


df_driver = pd.merge(df_vehicle, dfnames, how='left', on='pid').copy()
df_driver = df_driver.rename(columns={"pid": "pp"}).copy()


#available_vid = fleet_data_rounded['vid'].unique()



# Layout
layout = html.Div([

    #dict(
     #   autosize=True,
      #  height=450,
       # font=dict(color="#191A1A"),
        #titlefont=dict(color="#191A1A", size='14'),
        #margin=dict(
         #   l=45,
          #  r=15,
           # b=45,
            #t=35
        #)
    #),
    # Title - Row
    html.Div(
        [
            html.H1(
                'Test App',
                style={'font-family': 'Helvetica',
                       "margin-left": "20",
                       "margin-bottom": "0"},
                className='eight columns',
            )
        ],
        className='row'
    ),

    #block 2
    html.Div([
        dcc.Store(id = 'memory'),
        html.H3('Vehicle Overview'),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='graph'
                                  ),
                    ], className="four columns", style={'margin-top': 35,
                                                        'padding': '15',
                                                        'border': '1px solid #C6CCD5'}
                ),
                html.Div(
                    [
                        html.P('Vehicle Number:'),
                        dcc.Dropdown(
                                id = 'filter_x',
                                options=[{'label': i, 'value': i} for i in sorted(df_vehicle['vid'])],
                                value=''
                        ),
                    ],
                    className='three columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.P('Price:'),
                        dcc.Dropdown(
                                id = 'filter_y',
                                options=[
                                    {'label': 'No filter', 'value': 0},
                                    {'label': '1 to 20k', 'value': 1},
                                    {'label': '20k to 30k', 'value': 2},
                                    {'label': '30k+', 'value': 3}
                                ],
                                value='0'
                        )
                    ],
                    className='filter',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.Button('Reset Chart', id='button_chart')
                    ],
                    className='one columns',
                    style={'margin-top': '40'}
                ),
                html.Div(
                    [
                        html.Button('Previous Level', id='back_button')
                    ],
                    className='one columns',
                    style={'margin-top': '40', 'margin-left':'50'}
                )
            ],
            className='row'
        ),

        html.Div(
            [
                html.Div(id = 'table-box'),
                html.Div(dt.DataTable(id = 'table', data=[{}]), style={'display': 'none'})
            ], className = 'row'
        )
    ], className = 'row',  style = {'margin-top': 20, 'border':
                                    '1px solid #C6CCD5', 'padding': 15,
                                    'border-radius': '5px'})
], style = {'padding': '25px',})

