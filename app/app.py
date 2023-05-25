import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from flask_caching import Cache
import plotly.io as pio
import pymssql
pio.templates.default = "plotly_white"
import warnings
warnings.filterwarnings('ignore')

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.YETI])
server = app.server
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache'
})
def server_layout():
    return dash.page_container

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
            justified='around'
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Energy Demand",
                         style={'fontSize':40, 'textAlign':'center'}),
                xs=12, sm=12, md=8, lg=8, xl=8, xxl=8)
    ],justify='around'),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar,
                ],xs=12, sm=12, md=10, lg=10, xl=10, xxl=10),
        ], justify='around'
    ),
    html.Br(),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                [
                    server_layout(),
                ], xs=8, sm=8, md=10, lg=12, xl=12, xxl=12)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run()
