import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='Home',  # name of page, commonly used as name of link
                   title='Index',  # title that appears on browser's tab
                   image='pg1.png',  # image in the assets folder
                   description='Histograms are the new bar charts.'
)

# page 1 data
df = px.data.gapminder()

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4('Write summary')
                    ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='main',
                                  figure= {}

                                                      )
                    ], width=12
                )
            ]
        )
    ]
)


