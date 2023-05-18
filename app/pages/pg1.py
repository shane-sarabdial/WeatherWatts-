import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='Home',  # name of page, commonly used as name of link
                   title='Index',  # title that appears on browser's tab
                   image='pg1.png',  # image in the assets folder
                   description='Histograms are the new bar charts.'
                   )

# page 1 data
geo = pd.read_csv(r'app\Data\geo3.csv')

geo_year = geo.query('Year == 2015')
fig_geo = px.scatter_mapbox(geo_year, lat='Lat', lon='Long', title="Temperature by City From 2015 to 2023",
                            center=dict(lat=35.09024, lon=-95.712891),
                            zoom=2.7, mapbox_style="open-street-map", color_continuous_midpoint=50, opacity=.5,
                            color_continuous_scale='sunsetdark', size='Dew', color='Temperature',
                            text='City', labels='City',size_max=25)


col_options = [
            'Temperature','Dew', 'Humidity', 'Percipitation Probability', 'Snow', 'Wind Speed',
            'Sea Level Pressure', 'Cloud Cover','Solar Radiation', 'UV Index',]
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
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(id='year', options=[{'label': x, 'value': x} for x in range(2015, 2024)],
                                     placeholder='Year', value=2015, maxHeight=150)
                    ], width={'size': 3, 'offset': 2}
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(id='col', options=[{'label': x, 'value': x} for x in col_options],
                                     placeholder='Temperature', maxHeight=150, value='Temperature')
                    ], width={'size': 3, 'offset': 0}
                )

            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='map',
                                  figure=fig_geo, style={'width': '82vw', 'height': '60vh'}

                                  )
                    ], width={'size': 10, 'offset': 1}
                )
            ]
        )
    ]
)
@callback(
    Output('map', 'figure'),
    Input('year', 'value'),
    Input('col', 'value')
)
def update_map(year, col):
    geo_year_1 = geo.query(f'Year == {year}')
    fig_geo = px.bar(geo_year_1, x='City', y=col)
    print(year)
    print(col)
    return fig_geo

