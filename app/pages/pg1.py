import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from PIL import Image

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='Home',  # name of page, commonly used as name of link
                   title='Index',  # title that appears on browser's tab
                   image='pg1.png',  # image in the assets folder
                   description='Histograms are the new bar charts.'
                   )

# page 1 data
iso = pd.read_csv('./Data/iso.csv')
geo = pd.read_csv('./Data/geo3.csv')

fig_iso = px.choropleth(iso, locations="State",
                        color="ISO",  # lifeExp is a column of gapminder
                        hover_name="ISO",  # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma,
                        locationmode='USA-states',
                        scope='usa',
                        labels={'State': 'State'},
                        color_discrete_sequence=px.colors.qualitative.Pastel,

                        )
fig_iso.add_scattergeo(
    locations=iso['State'],
    locationmode='USA-states',
    text=iso['State'],
    mode='text',
    showlegend=False,
    hoverinfo='none',
)
fig_geo = px.scatter_geo(geo, lon='Long', lat='Lat',
                         hover_data=['Year', 'Temperature', 'Dew', 'Wind Speed', 'Cloud Cover',
                                     'UV Index'], scope='usa', hover_name='City',
                         color_discrete_sequence=['rgb(10, 10, 10)'], size='Temperature', size_max=7)

fig_geo.add_scattergeo(
    lon=geo['Long'],
    lat=geo['Lat'], marker_size=8, marker_color='rgb(10, 10, 10)', showlegend=False,
)
fig_iso.update_layout(
    title={'text': 'ISO Regions',
           'xanchor': 'center',
           'yanchor': 'top',
           'x': 0.5,
           'font_size': 40, })
fig_iso.add_trace(fig_geo.data[0])
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown('''In this project we aim to predict and identify key features that can impact
                         energy demand in the United States. We used weather and a energy ETF.
                         [XLE](https://finance.yahoo.com/quote/XLF?p=XLF&.tsrc=fin-srch) is a index that tracks the
                         performance of in the energy industry. Our focus are on the states of California, New York,
                         Texas and Florida. The weather data was taken from a major city in each state. They are 
                         Austin, Texas, New York City, NY, Tampa, Florida and Los Angeles, California. In the US there
                         are non-profit organizations that facilitate fair competition and ensure non-discriminatory
                         access to energy, they are called Independent System Operators 
                         [ISO](https://en.wikipedia.org/wiki/Regional_transmission_organization_(North_America)). With
                         the exception of Florida the other 3 states are ISOs. To get the full details of our mythology
                         in constructing our model vist our [github](https://github.com/shane-sarabdial/WeatherWatts-).
                         ''', style={'textAlign': 'center'}
                                     )
                    ], xs=12, sm=12, md=11, lg=8, xl=8, xxl=8
                )
            ], justify='around'
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='map',
                                  figure=fig_iso, style={'width': '60vw', 'height': '60vh'}

                                  )
                    ], xs=12, sm=12, md=8, lg=8, xl=8, xxl=8
                )
            ], justify='around'
        )
    ]
)
