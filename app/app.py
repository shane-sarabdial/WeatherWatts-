import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from flask_caching import Cache
import plotly.io as pio
import pymssql
from config import database
from config import table
from config import username
from config import password
from config import serverdb
pio.templates.default = "plotly_white"

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])
server = app.server
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache'
})

timeout = 20
sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="nav justify-content-center"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            horizontal=True,
            pills=True,
            className="bg-light",
            justified='center'
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Energy Demand",
                         style={'fontSize':40, 'textAlign':'center'}),width=12)
    ],justify='left'),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar,
                ], width={'size': 6, 'offset': 3},),
        ]
    ),
    html.Br(),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run(debug=True)
