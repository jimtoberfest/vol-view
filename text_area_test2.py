import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from dash import dash_table
import pandas as pd

app = dash.Dash(__name__)

# *Functions to use...

# Function to take multi-line text input from TextArea and create a DataFrame

block_columns = ['Time', 'Strike', 'Term', 'Instrument Type', 'Strategy', 'Type', 'CC',
                 'Product', 'Description', 'Price', 'Qty', 'Watch', 'RFQ', 'Add Deal',
                 'Undrl. Bid', 'Undrl. Offer', 'Impl. Vol', 'Δ', 'Category']


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
        style={'width': '100%', 'height': 200},
    ),
    html.Button('Submit', id='textarea-state-example-button', n_clicks=0),
    html.Div(id='textarea-state-example-output',
             style={'whiteSpace': 'pre-line'}),
    html.Div(
        dash_table.DataTable(
            id='blocks_table',
            data=(),
            columns=[{"name": i, "id": i} for i in block_columns],
            )
    )

])


@app.callback(
    Output('textarea-state-example-output', 'children'),

    Output('blocks_table', 'data'),  # ! New Output!

    Input('textarea-state-example-button', 'n_clicks'),
    State('textarea-state-example', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        print('type: ', type(value))
        # dfs = pd.read_csv(value, sep='\t')
        # print('value:', list(value))
        # print(value)
        print('\nrepr: ', repr(value))

        df_blocks = input2df(value)
        print('\n', df_blocks)

        return 'You have entered: \n{}\n{}'.format(type(value), ''), df_blocks.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
