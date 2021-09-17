import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
from dash import dash_table
from dash.html.H4 import H4
import pandas as pd

app = dash.Dash(__name__)

# *Functions to use...

# Function to take multi-line text input from TextArea and create a DataFrame

records = {}
g_records = {}

def input2df(estr, sep='\t', lineterm='\n', header=True):
    dat = [x.split(sep) for x in estr.split(lineterm)]
    cdf = pd.DataFrame(dat)
    if header:
        new_header = cdf.iloc[0]
        cdf.columns = new_header
        cdf.drop(index=cdf.index[0],
                 axis=0,
                 inplace=True)
    return cdf


app.layout = html.Div([
    dcc.Textarea(
        id='textarea-state-example',
        # value='Textarea content initialized\nwith multiple lines of text',
        value='',
        placeholder='Paste Data Here',
        style={'width': '100%', 'height': 100},
    ),
    html.Button('Submit', id='textarea-state-example-button', n_clicks=0),
    html.Div(id='textarea-state-example-output',
             style={'whiteSpace': 'pre-line'}),
# *-----------------------------------------------------------------------
    
    html.Hr(),

    html.Div([
        dcc.Tabs(id='tabs-example', value='tab-1', children=[
            dcc.Tab(label='Raw Table', value='tab-1'),
            dcc.Tab(label='Sorted by Volume', value='tab-2'),
        ]),

        html.Div(id='tabs-example-content'),
        
        html.Hr(),
    ]),

])


@app.callback(Output('tabs-example-content', 'children'),
              Input('textarea-state-example-button', 'n_clicks'),
              State('textarea-state-example', 'value'),
              Input('tabs-example', 'value')

              )
def render_content(n_clicks, value, tab):

    if n_clicks > 0:
        print('n is over 1')
        try:
            df_blocks = input2df(value)
            df_blocks['Qty'] = df_blocks['Qty'].apply(pd.to_numeric, errors='coerce')
            df_blocks['Strike'] = df_blocks['Strike'].apply(pd.to_numeric, errors='coerce')
            df_blocks['Price'] = df_blocks['Price'].apply(pd.to_numeric, errors='coerce')
            records = df_blocks.to_dict('records')
            columns = [{"name": i, "id": i, } for i in (df_blocks.columns)]
            print(df_blocks.head())
            
            g1 = df_blocks.groupby(['Type', 'Instrument Type', 'Term','CC','Description']).sum()
            g2 = g1.add_suffix('_Count').reset_index()
            g2 = g2.sort_values('Qty_Count', ascending=False)
            g2 = g2[['Type','Instrument Type', 'Term', 'CC', 'Description','Qty_Count']]
            print(g2.head())
            
            g_records = g2.to_dict('records')
            g_columns = [{"name": i, "id": i, } for i in (g2.columns)]
            print(g1)

            
        except:
            print('no rawdata')
            df_blocks = pd.DataFrame()

    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1'),
            dash_table.DataTable(
                data=records, columns=columns, page_size=15, sort_action='native', filter_action='native')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2'),
            dash_table.DataTable(
                data=g_records, columns=g_columns, page_size=15, sort_action='native', filter_action='native')

        ])
    else:
        print('else...')
        return html.Div([
            html.H3('NOTHING!!!')
        ])

# ?--------------------------------------------------------------------
# @app.callback(
#     Output('textarea-state-example-output', 'children'),
#     Input('textarea-state-example-button', 'n_clicks'),
#     State('textarea-state-example', 'value')
# )
# def update_output(n_clicks, value):
#     if n_clicks > 0:
#         print('type: ', type(value))
#         # dfs = pd.read_csv(value, sep='\t')
#         # print('value:', list(value))
#         # print(value)
#         print('\nrepr: ', repr(value))

#         df_blocks = input2df(value)
#         print('\n', df_blocks.dtypes)

#         # , df_blocks.to_dict('records')
#         return 'You have entered: \n{}\n{}'.format(type(value), '')

# ?--------------------------------------------------------------------

# @ app.callback(
#     Output('blocks_table', 'children'),
#     Input('textarea-state-example-button', 'n_clicks'),
#     State('textarea-state-example', 'value')

# )
# def update_datatable(n_clicks, value):
#     if n_clicks > 0:
#         df_blocks = input2df(value)
#         df_blocks['Qty'] = df_blocks['Qty'].apply(
#             pd.to_numeric, errors='coerce')
#         df_blocks['Strike'] = df_blocks['Strike'].apply(
#             pd.to_numeric, errors='coerce')
#         df_blocks['Price'] = df_blocks['Price'].apply(
#             pd.to_numeric, errors='coerce')
#         df_blocks.fillna(0, inplace=True)
#         # print('\n', df_blocks.dtypes)  # ! This is for Debugging
#         records = df_blocks.to_dict('rows')
#         columns = [{"name": i, "id": i, } for i in (df_blocks.columns)]
#         return html.Div([
#             H4('Title'),

#             html.Div([dcc.Dropdown(id='groupby-drop', multi=True,  # new to True from False
#                                    options=[{'label': i, 'value': i}
#                                             for i in df_blocks.columns],
#                                    placeholder='Select for GroupBy'
#                                    #    style = {"width": "50%"}
#                                    ),
#                       html.Button(
#                           'Group', id='block-groupby-button', n_clicks=0),
#                       html.Button('Sum', id='sum-groupby-button', n_clicks=0)],
#                      style={"width": "50%", "display": "inline-block"}
#                      ),

#             html.Hr(),
#             dash_table.DataTable(data=records, columns=columns, page_size=15)
#         ])


if __name__ == '__main__':
    app.run_server(debug=True)
