import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
from dash import dash_table
from dash.html.H4 import H4
import pandas as pd
import dash_bootstrap_components as dbc

app = dash.Dash(
    external_stylesheets=[dbc.themes.FLATLY]
)

nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Active", active=True, href="#")),
        dbc.NavItem(dbc.NavLink("A link", href="#")),
        dbc.NavItem(dbc.NavLink("Another link", href="#")),
        dbc.NavItem(dbc.NavLink("Disabled", disabled=True, href="#")),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("Item 1"), dbc.DropdownMenuItem("Item 2")],
            label="Dropdown",
            nav=True,
        ),
    ]
)


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Vol View", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="TurboForce",
    brand_href="#",
    color="light",
    dark=False,
    expand=True,
    brand_style={font-family: 'Lato', color:grey, font-size: "24px"}
    
    
    
    # ?Allowed arguments: brand, brand_external_link, brand_href, brand_style, children, className, color, dark, expand, fixed, fluid, id, key, light, links_left, loading_state, sticky, style
)

app.layout = html.Div([
    nav,
    navbar
])

if __name__ == "__main__":
    app.run_server()