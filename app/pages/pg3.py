import dash
from dash import dcc, html, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go

pio.templates.default = "seaborn"
import pickle
from datetime import date
import datetime
from flask_caching import Cache

dash.register_page(__name__,
                   path='/newyork',  # represents the url text
                   name='NewYork',  # name of page, commonly used as name of link
                   title='NewYork'  # epresents the title of browser's tab
                   )
app = dash.get_app()
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
TIMEOUT = 300

# page 2 data
df_ny = pd.read_parquet('Data/NY/NY_df.parquet')
df_ny.rename(columns={'value': 'Actual', 'prediction': 'Prediction'}, inplace=True)
fig1_ny = px.box(df_ny, x='hour', y='Actual', title='Range of Energy Demand by Hour', )
fig1_ny.update_layout(title=dict(
    font_size=20, x=0.5),
    yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts', title_font_size=15),
    xaxis=dict(tickfont_size=13, title_font_size=20))

@cache.memoize(timeout=TIMEOUT)
def create_scatter():
    fig2_ny = px.scatter(data_frame=df_ny, x=df_ny.index, y=['Actual', 'Prediction'],
                      opacity=.5, size_max=.2, render_mode='webgl', )

    # Update the layout
    fig2_ny.update_layout(
        title='Actual VS Prediction',
        xaxis=dict(title='Period', title_font_size=20),
        yaxis=dict(title='Demand in Megawatt Hours', title_font_size=20)    )
    return fig2_ny

filename = R'Data\NY\model_NY.pkl'
with open(filename, 'rb') as f:
    model = pickle.load(f)
fi_ny = pd.DataFrame(data=model.feature_importances_,
                     index=model.feature_name_,
                     columns=['importance'])
fi_ny = fi_ny.sort_values('importance', ascending=False)[:20]
fig3_ny = px.bar(fi_ny, y=fi_ny.index, x='importance', log_x=True)

week = ['2021-11-2', '2021-11-9']
df2_ny = df_ny.loc[(df_ny.index > week[0]) & (df_ny.index < week[1])][['Actual', 'Prediction']]
fig4_ny = px.line(data_frame=df2_ny, x=df2_ny.index, y=['Actual', 'Prediction'], title='One Week of Data')
fig4_ny.update_layout(title=dict(
    font_size=20, x=0.5),
    yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
    xaxis=dict(tickfont_size=13, title='Period', title_font_size=20))

layout = html.Div(
    [
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='prediction_ny',
                              figure=create_scatter(), style={'width': '90vw', 'height': '75vh'})
                ], width={'size': 11, 'offset': 0},
            ),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Dropdown(id='freq_ny', multi=False, value='hour',
                                 options=[{'label': 'Hour', 'value': 'hour'},
                                          {'label': 'Month', 'value': 'month'},
                                          {'label': 'Day of the week', 'value': 'days'},
                                          {'label': 'Quarter', 'value': 'quarter'},
                                          {'label': 'Day of year', 'value': 'dayofyear'},
                                          ], )

                ], width={'size': 4, 'offset': 1},
            ),
            dbc.Col(
                [
                    dcc.DatePickerSingle(id='cal_ny',
                                         clearable=True,
                                         persistence=True,
                                         month_format='MM-DD-YYYY',
                                         placeholder=' 11/02/2021',
                                         date=date(2021, 11, 9),
                                         with_portal=True,
                                         min_date_allowed=date(2021, 11, 2),
                                         max_date_allowed=date(2023, 4, 29), )
                ], width={'size': 2, 'offset': 3},
            ),
        ], justify='start', align='center'),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='freq_box_ny',
                              figure=fig1_ny, style={'width': '40vw', 'height': '75vh'})
                ], width={'size': 6, 'offset': 0}
            ),
            dbc.Col(
                [
                    dcc.Graph(id='week_ny',
                              figure=fig4_ny, style={'width': '55vw', 'height': '75vh'})
                ], width={'size': 6, 'offset': 0}
            ),
        ]),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='fi_ny',
                              figure=fig3_ny, style={'width': '40vw', 'height': '75vh'})
                ], width={'size': 6, 'offset': 0}

            ),
            dbc.Col(
                [
                dbc.CardBody(
                    html.P('fsdfds')
                ),
                    # dcc.Graph(id='main',
                    #           figure={})
                ], width={'size': 5, 'offset': 1},
            )
        ]),
    ])


@callback(
    Output('freq_box_ny', 'figure'),
    [Input('freq_ny', 'value')],
    [State("freq_ny", "options")],
)
def update_graph(value, opt):
    label = [x['label'] for x in opt if x['value'] == value]
    label = label[0]
    fig1 = px.box(df_ny, x=value, y='Actual', title=f'Range of Energy Demand by {label}')
    fig1.update_layout(title=dict(
        font_size=20, x=0.5),
        yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
        xaxis=dict(tickfont_size=13, title=label, title_font_size=20))
    return fig1


@callback(
    Output('week_ny', 'figure'),
    Input('cal_ny', 'date'),
)
def update_week(date_enter):
    aDate = datetime.datetime.strptime(date_enter, "%Y-%m-%d")
    oneWeek = datetime.timedelta(weeks=1)
    new_date = aDate + oneWeek
    tx2 = df_ny.loc[(df_ny.index > date_enter) & (df_ny.index < new_date)][['Actual', 'Prediction']]
    fig4 = px.line(data_frame=tx2, x=tx2.index, y=['Actual', 'Prediction'], title='One Week of Data')
    fig4.update_layout(title=dict(
        font_size=20, x=0.5),
        yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
        xaxis=dict(tickfont_size=13, title='Period', title_font_size=20))
    return fig4
