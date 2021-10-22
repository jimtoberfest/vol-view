import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
from dash import dash_table
from dash.html.H4 import H4
import pandas as pd

app = dash.Dash(__name__)
server = app.server  # !Comment this out to work locally

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
    # html.Button('Download As Excel', id='textarea-state-excel-button', n_clicks=0),
    html.Div(id='textarea-state-example-output',
             style={'whiteSpace': 'pre-line'}),
    # html.Button('Download As Excel', id='excel_button', n_clicks=0),
    #! html.Button("Download Excel", id="btn_xlsx"),
    #! dcc.Download(id="download-dataframe-xlsx"),
# *-----------------------------------------------------------------------
    
    html.Hr(),

    html.Div([
        dcc.Tabs(id='tabs-example', value='tab-1', children=[
            dcc.Tab(label='Raw Table', value='tab-1'),
            dcc.Tab(label='Sorted by Volume', value='tab-2'),
            dcc.Tab(label='Summation', value='tab-3'),
            dcc.Tab(label='Strips(Beta)', value='tab-4')
        ]),

        html.Div(id='tabs-example-content'),
        
        html.Hr(),
    ]),

])


@app.callback(Output('tabs-example-content', 'children'),
            #   Output("download-dataframe-xlsx", "data"),
              Input('textarea-state-example-button', 'n_clicks'),
            #   Input("btn_xlsx", "n_clicks"),
              State('textarea-state-example', 'value'),
              Input('tabs-example', 'value'),
              prevent_initial_call=True,

              )
def render_content(n_clicks, value, tab):

    if n_clicks > 0:
        print('n is over 1')
        try:
            df_blocks = input2df(value)
            
            #! Following code added to deal with commas in large numbers.
            # df_blocks.to_csv('df_blocks_pre_manipulation.csv', index=False) #for testing
            df_blocks['Qty'] = (df_blocks['Qty'].replace(',','', regex=True).astype(float))            
            
            df_blocks['Qty'] = df_blocks['Qty'].apply(pd.to_numeric, errors='coerce')
            df_blocks['Strike'] = df_blocks['Strike'].apply(pd.to_numeric, errors='coerce')
            df_blocks['Price'] = df_blocks['Price'].apply(pd.to_numeric, errors='coerce')
            records = df_blocks.to_dict('records')
            columns = [{"name": i, "id": i, } for i in (df_blocks.columns)]
            print('df: ',df_blocks.head())
            
            g1 = df_blocks.groupby(['Type', 'Instrument Type', 'Term','CC','Description']).sum()
            g2 = g1.add_suffix('_Count').reset_index()
            g2 = g2.sort_values('Qty_Count', ascending=False)
            g2 = g2[['Type','Instrument Type', 'Term', 'CC', 'Description','Qty_Count']]
            print('g2:', g2.head())
            
            g_records = g2.to_dict('records')
            g_columns = [{"name": i, "id": i, } for i in (g2.columns)]
            
            g3 = g1.groupby(['Type','CC']).sum()
            g3 = g3.add_suffix('_Count').reset_index()
            g3 = g3[['Type', 'CC', 'Qty_Count']]
            
            summation_records = g3.to_dict('records')
            summation_columns = [{"name": i, "id": i, } for i in (g3.columns)]
            
            
            # *Build out fourth Tab for strips
            df_strip = df_blocks.copy() #! Change to fit df_blocks
            # df_strip['Qty'] = pd.to_numeric(df_strip['Qty'], errors='coerce')

            strip_totals = df_strip.groupby(['Time', 'Strike', 'Strategy'])['Qty'].transform('sum').fillna(0)
            strip_counts = df_strip.groupby(['Time', 'Strike', 'Strategy'])['Qty'].transform('count').fillna(0)

            df_strip['Qty_Strip'] = strip_totals
            df_strip['Strip_Count'] = strip_counts
            df_strip = df_strip.sort_values(['Qty_Strip', 'Strike'], ascending=False).head(100)
            df_strip = df_strip[df_strip['Strip_Count'] > 2]

            strip_first = df_strip.groupby(['Time', 'Strike', 'Strategy'])['Term'].transform('first').fillna(0)
            strip_last = df_strip.groupby(['Time', 'Strike', 'Strategy'])['Term'].transform('last').fillna(0)

            df_strip['strip_first'] = strip_first
            df_strip['strip_last'] = strip_last
            df_strip['Strip_Term'] = strip_first + " : " + strip_last


            df_strip_agg = df_strip.groupby(['Time','Type','CC', 'Strip_Term', 'Strategy', 'Strike'])['Qty'].sum().reset_index()
            df_strip_agg = df_strip_agg.sort_values('Qty', ascending=False)
            df_strip_agg = df_strip_agg.reset_index(drop=True)

            strips_records = df_strip_agg.to_dict('records')
            strips_columns = [{"name": i, "id": i, } for i in (df_strip_agg.columns)]
            
        except:
            print('no rawdata')
            df_blocks = pd.DataFrame()

    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1'),
            html.Button("Tab 1 Button", id="btn_T1"),
            dash_table.DataTable(
                data=records, columns=columns, page_size=15, sort_action='native', filter_action='native')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2'),
            # dash_table.DataTable(  # *g3 summation Table
            #     data=summation_records, columns=summation_columns, page_size=15, sort_action='native', filter_action='native'),
            dash_table.DataTable(
                data=g_records, columns=g_columns, page_size=15, sort_action='native', filter_action='native')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3'),
            dash_table.DataTable(  # *g3 summation Table
                data=summation_records, columns=summation_columns, page_size=15, sort_action='native', filter_action='native')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 3'),
            dash_table.DataTable(  # *g4 strip Table
                data=strips_records, columns=strips_columns, page_size=15, sort_action='native', filter_action='native')
        ])    
    else:
        print('else...')
        return html.Div([
            html.H3('NOTHING!!!')
        ])
#!  EXCEL EXPORT FUNCTIONS?
# @app.callback(
#     Output("download-dataframe-xlsx", "data"),
#     Input("btn_xlsx", "n_clicks"),
#     State('textarea-state-example', 'value'),
#     prevent_initial_call=True,
# )
# def make_excel(n_clicks, value):
#     if n_clicks > 0:
#         print('n_xls is over 1')
#         df_blocks = input2df(value)
#         return dcc.send_data_frame(df_blocks.to_excel, "mydf.xlsx", sheet_name="raw_data")



'''
def make_excel(n_clicks, value):
    if n_clicks > 0:
        print('n_xls is over 1')
        df_raw = input2df(value)
        
        df_blocks = df_raw.copy()
        
        df_blocks['Qty'] = (df_blocks['Qty'].replace(',','', regex=True).astype(float))            
            
        df_blocks['Qty'] = df_blocks['Qty'].apply(pd.to_numeric, errors='coerce')
        df_blocks['Strike'] = df_blocks['Strike'].apply(pd.to_numeric, errors='coerce')
        df_blocks['Price'] = df_blocks['Price'].apply(pd.to_numeric, errors='coerce')
        # print(df_blocks.head())
        
        g1 = df_blocks.groupby(['Type', 'Instrument Type', 'Term','CC','Description']).sum()
        g2 = g1.add_suffix('_Count').reset_index()
        g2 = g2.sort_values('Qty_Count', ascending=False)
        g2 = g2[['Type','Instrument Type', 'Term', 'CC', 'Description','Qty_Count']]
        print(g2.head())
        
        def to_xlsx(bytes_io):
            xlsx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
            for i in my_report_name:
                df = make_report(i, my_start_date, my_end_date)
                df.to_excel(xlsx_writer, index=False, sheet_name=i)
            xlsx_writer.save()
        
        return send_bytes(to_xlsx, file_name)
        
        
        
        
        return dcc.send_data_frame(df_raw.to_excel, "mydf.xlsx", sheet_name="raw_data")


>>> df2 = df1.copy()
>>> with pd.ExcelWriter('output.xlsx') as writer:  # doctest: +SKIP
...     df1.to_excel(writer, sheet_name='Sheet_name_1')
...     df2.to_excel(writer, sheet_name='Sheet_name_2')
'''           

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
