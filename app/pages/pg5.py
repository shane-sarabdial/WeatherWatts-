import dash
from dash import dcc, html, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import pymssql
from config import database
from config import username
from config import password
from config import serverdb

template = pio.templates.default = "plotly_white"
import pickle
from datetime import date
import datetime
from flask_caching import Cache

dash.register_page(__name__,
                   path='/california',  # represents the url text
                   name='California',  # name of page, commonly used as name of link
                   title='California'  # epresents the title of browser's tab
                   )
app = dash.get_app()
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
TIMEOUT = 240

# page 2 data
df_ca = pd.read_parquet(r'app\Data\CA\CA_df.parquet')
df_ca.rename(columns={'value': 'Actual', 'prediction': 'Prediction'}, inplace=True)
fig1_ca = px.box(df_ca, x='hour', y='Actual', title='Range of Energy Demand by Hour',
                 color_discrete_sequence=['rgb(95, 70, 144)'])
fig1_ca.update_layout(title=dict(
    font_size=20, x=0.55),
    yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts', title_font_size=15),
    xaxis=dict(tickfont_size=13, title_font_size=20, title='Hour'),
    margin=dict(t=33, b=20, r=20),
    template=template
)


@cache.memoize(timeout=TIMEOUT)
def create_scatter():
    fig2_ca = px.scatter(data_frame=df_ca, x=df_ca.index, y=['Actual', 'Prediction'],
                         opacity=.5, size_max=.2, render_mode='webgl', title='Actual VS Prediction',
                         color_discrete_map={"Actual": 'rgb(29, 105, 150)', "Prediction": 'rgb(204, 80, 62)'})

    # Update the layout
    fig2_ca.update_layout(
        title=dict(font_size=30),
        xaxis=dict(title='Period', title_font_size=25, tickfont_size=15, ),
        yaxis=dict(title='Demand in Megawatt Hours', title_font_size=25, tickfont_size=15, ),
        margin=dict(t=50, b=50, ),
        template=template
    )
    return fig2_ca


filename = R'app\Data\CA\model_CA.pkl'
with open(filename, 'rb') as f:
    model = pickle.load(f)
fi_ca = pd.DataFrame(data=model.feature_importances_,
                     index=model.feature_name_,
                     columns=['importance'])
fi_ca = fi_ca.sort_values('importance', ascending=False)[:20]
fig3_ca = px.bar(fi_ca, y=fi_ca.index, x='importance', log_x=False, title='Top 20 Important Features',
                 color_discrete_sequence=['rgb(56, 166, 165)'])
fig3_ca.update_layout(
    title=dict(font_size=20, x=0.8),
    xaxis=dict(title='Importance', title_font_size=18),
    yaxis=dict(title='Features', title_font_size=18),
    margin=dict(t=30, b=20, r=20),
    template=template
)

week = ['2021-11-2', '2021-11-9']
df2_ca = df_ca.loc[(df_ca.index > week[0]) & (df_ca.index < week[1])][['Actual', 'Prediction']]
fig4_ca = px.line(data_frame=df2_ca, x=df2_ca.index, y=['Actual', 'Prediction'], title='One Week of Data',
                  color_discrete_map={"Actual": 'rgb(29, 105, 150)', "Prediction": 'rgb(204, 80, 62)'})
fig4_ca.update_layout(title=dict(
    font_size=20, x=0.45),
    yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
    xaxis=dict(tickfont_size=13, title='Period', title_font_size=20),
    margin=dict(t=38, b=20),
    template=template)


def get_data_sql():
    conn = pymssql.connect(serverdb, username, password, database)
    cursor = conn.cursor()
    query = """SELECT TOP (72) *
            FROM dbo.future_data__CA
            ORDER BY [DATE] DESC"""
    df = pd.read_sql(query, conn)
    df.index = pd.to_datetime(df.Date)
    df = df.drop(['State', 'Date'], axis=1)
    df = df.sort_index()
    return df


CA_pred = get_data_sql()
CA_pred['pred'] = model.predict(CA_pred)
fig5_ca = px.line(data_frame=CA_pred, x=CA_pred.index, y='pred', title='Predicting Demand in 3 Days',
                  color_discrete_sequence=['rgb(225, 124, 5)'])
fig5_ca.update_layout(title=dict(
    font_size=20, x=0.45),
    yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
    xaxis=dict(tickfont_size=13, title='Period', title_font_size=20),
    margin=dict(t=38, b=20),
    template=template)

layout = html.Div(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.H1('ERCOT'),
                    dcc.Markdown("""The Electric Reliability Council of Texas [(ERCOT)](https://www.ercot.com/about) 
                    is an independent system operator (ISO) for the state of Texas. They supply power to about 90% of
                     the states population. """),
                    # html.P('The Electric Reliability Council of Texas (ERCOT)'),
                    html.H2('Model Performance'),
                    dcc.Markdown("""The Root Mean Square Error (RMSE) and Mean Absolute Error (MAE) were 3484.53 and 
                    2606.52 respectively. From the graphs we can see that the model is under-predicting on average 
                    about ~3000  megawatt hours. 
                      """),
                ], width={'size': 10, 'offset': 1},
            ),
        ], ),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='prediction_ca',
                              figure=create_scatter(), style={'width': '82vw', 'height': '60vh'})
                ], width={'size': 9, 'offset': 1},
            ),
        ], ),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Dropdown(id='freq_ca', multi=False, value='hour',
                                 options=[{'label': 'Hour', 'value': 'hour'},
                                          {'label': 'Month', 'value': 'month'},
                                          {'label': 'Day of the Week', 'value': 'days'},
                                          {'label': 'Quarter', 'value': 'quarter'},
                                          {'label': 'Day of Year', 'value': 'dayofyear'},
                                          ],
                                 style=dict(border='1px solid black', width='100%', )
                                 )

                ], width={'size': 3, 'offset': 2},
            ),
            dbc.Col(
                [
                    dcc.DatePickerSingle(id='cal_ca',
                                         clearable=False,
                                         persistence=True,
                                         month_format='MM-DD-YYYY',
                                         placeholder=' 11/02/2021',
                                         date=date(2021, 11, 9),
                                         with_portal=True,
                                         min_date_allowed=date(2021, 11, 2),
                                         max_date_allowed=date(2023, 4, 29),
                                         style=dict(border='2px solid black', width='68.5%', ), )
                ], width={'size': 3, 'offset': 3}, className="text-center",
            ),
        ], style={'align-items': 'center', 'display': 'flex', 'justify-content': 'center'}),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='freq_box_ca',
                              figure=fig1_ca, style={'width': '40vw', 'height': '50vh'})
                ], width={'size': 5, 'offset': 1}
            ),
            dbc.Col(
                [
                    dcc.Graph(id='week_ca',
                              figure=fig4_ca, style={'width': '40vw', 'height': '50vh'})
                ], width={'size': 5, 'offset': 1}
            ),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='fi_ca',
                              figure=fig3_ca, style={'width': '40vw', 'height': '50vh'})
                ], width={'size': 5, 'offset': 1}

            ),
            dbc.Col(
                [
                    dcc.Graph(id='future_ca',
                              figure=fig5_ca, style={'width': '40vw', 'height': '50vh'})
                ], width={'size': 5, 'offset': 1},
            )
        ]),
    ])


@callback(
    Output('freq_box_ca', 'figure'),
    [Input('freq_ca', 'value')],
    [State("freq_ca", "options")],
)
def update_graph(value, opt):
    label = [x['label'] for x in opt if x['value'] == value]
    label = label[0]
    fig1_ca = px.box(df_ca, x=value, y='Actual', title=f'Range of Energy Demand by {label}',
                     color_discrete_sequence=['rgb(95, 70, 144)'])
    fig1_ca.update_layout(title=dict(
        font_size=20, x=0.55),
        yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
        xaxis=dict(tickfont_size=13, title=label, title_font_size=20),
        margin=dict(t=33, b=20, r=20),
        template=template
    )
    return fig1_ca


@callback(
    Output('week_ca', 'figure'),
    Input('cal_ca', 'date'),
)
def update_week(date_enter):
    aDate = datetime.datetime.strptime(date_enter, "%Y-%m-%d")
    oneWeek = datetime.timedelta(weeks=1)
    new_date = aDate + oneWeek
    ca2 = df_ca.loc[(df_ca.index > date_enter) & (df_ca.index < new_date)][['Actual', 'Prediction']]
    fig4_ca = px.line(data_frame=ca2, x=ca2.index, y=['Actual', 'Prediction'], title='One Week of Data',
                   color_discrete_map={"Actual": 'rgb(29, 105, 150)', "Prediction": 'rgb(204, 80, 62)'})
    fig4_ca.update_layout(title=dict(
        font_size=20, x=0.45),
        yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
        xaxis=dict(tickfont_size=13, title='Period', title_font_size=20),
        margin=dict(t=38, b=20),
        template=template)
    return fig4_ca
