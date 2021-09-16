import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

app = dash.Dash(__name__)

# *Functions to use...


def input2df(estr, sep='\t', lineterm='\n', set_header=True):
    dat = [x.split(sep) for x in estr.split(lineterm)]
    cdf = pd.DataFrame(dat)
    if set_header:
        new_header = cdf.iloc[0]
        cdf.columns = new_header
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
             style={'whiteSpace': 'pre-line'})
])


@app.callback(
    Output('textarea-state-example-output', 'children'),
    Input('textarea-state-example-button', 'n_clicks'),
    State('textarea-state-example', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        print('type: ', type(value))
        # dfs = pd.read_csv(value, sep='\t')
        # print('value:', list(value))
        print(value)
        print('\nrepr: ', repr(value))

        df_blocks = input2df(value)
        df_blocks.drop(index=df_blocks.index[0],
                       axis=0,
                       inplace=True)

        print(df_blocks)

        return 'You have entered: \n{}\n{}'.format(type(value), value)


if __name__ == '__main__':
    app.run_server(debug=True)
