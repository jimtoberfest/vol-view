import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
from dash import dash_table
from dash.html.H4 import H4
import pandas as pd
import numpy as np

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

    html.Hr(),

    html.Div([
        dcc.Tabs(id='tabs-example', value='tab-1', children=[
            dcc.Tab(label='Raw Table', value='tab-1'),
            dcc.Tab(label='Sorted by Volume', value='tab-2'),
            dcc.Tab(label='Summation', value='tab-3')
            # dcc.Tab(label='Strips(Beta)', value='tab-4')
        ]),

        html.Div(id='tabs-example-content'),
        
        html.Hr(),
    ]),

])


@app.callback(Output('tabs-example-content', 'children'),
              Input('textarea-state-example-button', 'n_clicks'),
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
            
            
            # *Raw Data DataFrame
            records = df_blocks.to_dict('records')
            columns = [{"name": i, "id": i, } for i in (df_blocks.columns)]
            print('df: ',df_blocks.head())
            
            
            # df_blocks['Strike'] = df_blocks['Strike'].apply(pd.to_numeric, errors='coerce')
            # df_blocks['Price'] = df_blocks['Price'].apply(pd.to_numeric, errors='coerce')
            
            # *Parse Description
            df_blocks['parsed'] = df_blocks['Description'].str.split(" ")
            df_blocks['contract'] = df_blocks['parsed'].str[0]
            df_blocks['strike'] = df_blocks['parsed'].str[1]
            df_blocks['strategy'] = df_blocks['parsed'].str[2]
            df_blocks['strategy_2'] = df_blocks['parsed'].str[3:]
            # df_blocks['contract'] = pd.to_datetime(df_blocks['contract'], format='%b%y')
            
            # *Summary Tab DataFrame
            df_summary = df_blocks.groupby(['Type', 'CC', 'contract' , 'strike', 'strategy'])['Qty'].sum().reset_index()
            df_summary = df_summary.sort_values('Qty', ascending=False)
            
            summary_records = df_summary.to_dict('records')
            summary_columns = [{"name": i, "id": i, } for i in (df_summary.columns)]
            
            # *Product Tab DataFrame
            df_product_summary = df_blocks.groupby('CC')['Qty'].sum().reset_index()
            df_product_summary = df_product_summary.sort_values('Qty', ascending=False)
            
            product_records = df_product_summary.to_dict('records')
            product_columns = [{"name": i, "id": i, } for i in (df_product_summary.columns)]
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            # !  Old Code...
            
            # g1 = df_blocks.groupby(['Type', 'Instrument Type', 'Term','CC','Description']).sum()
            # g2 = g1.add_suffix('_Count').reset_index()
            # g2 = g2.sort_values('Qty_Count', ascending=False)
            # g2 = g2[['Type','Instrument Type', 'Term', 'CC', 'Description','Qty_Count']]
            # print('g2:', g2.head())
            
            # g_records = g2.to_dict('records')
            # g_columns = [{"name": i, "id": i, } for i in (g2.columns)]
            
            # g3 = g1.groupby(['Type','CC']).sum()
            # g3 = g3.add_suffix('_Count').reset_index()
            # g3 = g3[['Type', 'CC', 'Qty_Count']]
            
            # summation_records = g3.to_dict('records')
            # summation_columns = [{"name": i, "id": i, } for i in (g3.columns)]
            
            
            # df_strip = df_blocks.copy() #! Change to fit df_blocks
            # df_strip['Qty'] = pd.to_numeric(df_strip['Qty'], errors='coerce')

            # strip_totals = df_strip.groupby(['Time', 'Strike', 'Strategy'])['Qty'].transform('sum').fillna(0)
            # strip_counts = df_strip.groupby(['Time', 'Strike', 'Strategy'])['Qty'].transform('count').fillna(0)

            # df_strip['Qty_Strip'] = strip_totals
            # df_strip['Strip_Count'] = strip_counts
            # df_strip = df_strip.sort_values(['Qty_Strip', 'Strike'], ascending=False).head(100)
            # df_strip = df_strip[df_strip['Strip_Count'] > 1]

            # strip_first = df_strip.groupby(['Time', 'Strike', 'Strategy'])['Term'].transform('first').fillna(0)
            # strip_last = df_strip.groupby(['Time', 'Strike', 'Strategy'])['Term'].transform('last').fillna(0)

            # df_strip['strip_first'] = strip_first
            # df_strip['strip_last'] = strip_last
            # df_strip['Strip_Term'] = strip_first + " : " + strip_last

            # # *New code converts string dates to timestamps to deal with seasonality edge cases in strips

            # df_strip['month_1'] = pd.to_datetime(df_strip['strip_first'], format='%b%y')
            # df_strip['month_2'] = pd.to_datetime(df_strip['strip_last'], format='%b%y')
            # df_strip['Strip_Length'] = ((df_strip['month_2'] - df_strip['month_1']) / np.timedelta64(1, 'M')).astype('int') + 1



            # df_strip_agg = df_strip.groupby(['Time','Type','CC', 'Strip_Term', 'Strategy', 'Strike', 'Strip_Length'])['Qty'].sum().reset_index()
            # df_strip_agg = df_strip_agg.sort_values('Qty', ascending=False)
            # df_strip_agg= df_strip_agg[df_strip_agg['Strip_Length'] > 1]
            # df_strip_agg = df_strip_agg.reset_index(drop=True)

            # df_strip_agg['Qty_per_Mo'] = df_strip_agg['Qty'] / df_strip_agg['Strip_Length']
            
            
            
            # strips_records = df_strip_agg.to_dict('records')
            # strips_columns = [{"name": i, "id": i, } for i in (df_strip_agg.columns)]
            
        except:
            print('no rawdata')
            df_blocks = pd.DataFrame()

    if tab == 'tab-1':
        return html.Div([
            html.H3('Raw Data'),
            dash_table.DataTable(
                data=records, columns=columns, page_size=15, sort_action='native', filter_action='native')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Sorted by Volume'),
            # dash_table.DataTable(  # *g3 summation Table
            #     data=summation_records, columns=summation_columns, page_size=15, sort_action='native', filter_action='native'),
            dash_table.DataTable(
                data=summary_records, columns=summary_columns, page_size=15, sort_action='native', filter_action='native')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Sorted by Product'),
            dash_table.DataTable(  # *g3 summation Table
                data=product_records, columns=product_columns, page_size=15, sort_action='native', filter_action='native')
        ])
    # elif tab == 'tab-4':
    #     return html.Div([
    #         html.H3('Strips'),
    #         dash_table.DataTable(  # *g4 strip Table
    #             data=strips_records, columns=strips_columns, page_size=15, sort_action='native', filter_action='native')
    #     ])    
    else:
        print('else...')
        return html.Div([
            html.H3('NOTHING!!!')
        ])







if __name__ == '__main__':
    app.run_server(debug=False)
