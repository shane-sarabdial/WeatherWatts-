import dash
from dash import dcc, html, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import pymssql
template = pio.templates.default = "plotly_white"
import pickle
from datetime import date
import datetime
from flask_caching import Cache
from dotenv import load_dotenv
import os
load_dotenv()
database = os.environ.get('database')
username = os.environ.get('username_watts')
password = os.environ.get('password')
serverdb = os.environ.get('serverdb')

dash.register_page(__name__,
                   path='/florida',  # represents the url text
                   name='Florida',  # name of page, commonly used as name of link
                   title='Florida',  # epresents the title of browser's tab
                   order=2
                   )
app = dash.get_app()
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
TIMEOUT = 240

# page 2 data
df_fl = pd.read_parquet('../Data/FL/FL_df.parquet')
df_fl.rename(columns={'value': 'Actual', 'prediction': 'Prediction'}, inplace=True)
fig1_fl = px.box(df_fl, x='hour', y='Actual', title='Range of Energy Demand by Hour',
                 color_discrete_sequence=['rgb(95, 70, 144)'])
fig1_fl.update_layout(title=dict(
    font_size=20, x=0.5),
    yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts', title_font_size=15),
    xaxis=dict(tickfont_size=13, title_font_size=20, title='Hour'),
    margin=dict(t=33, b=20, r=20),
    template=template
)
@cache.memoize(timeout=TIMEOUT)
def create_scatter():
    fig2_fl = px.scatter(data_frame=df_fl, x=df_fl.index, y=['Actual', 'Prediction'],
                         opacity=.5, size_max=.2, render_mode='webgl', title='Actual VS Prediction',
                         color_discrete_map={"Actual": 'rgb(29, 105, 150)', "Prediction": 'rgb(204, 80, 62)'})

    # Update the layout
    fig2_fl.update_layout(
        title=dict(font_size=30, x=.5),
        xaxis=dict(title='Period', title_font_size=25, tickfont_size=15, ),
        yaxis=dict(title='Demand in Megawatt Hours', title_font_size=20, tickfont_size=15, ),
        margin=dict(t=50, b=50, ),
        template=template
    )
    return fig2_fl


filename = '../Data/FL/model_FL.pkl'
with open(filename, 'rb') as f:
    model = pickle.load(f)
fi_fl = pd.DataFrame(data=model.feature_importances_,
                     index=model.feature_name_,
                     columns=['importance'])
fi_fl = fi_fl.sort_values('importance', ascending=False)[:20]
fig3_fl = px.bar(fi_fl, y=fi_fl.index, x='importance', log_x=False, title='Top 20 Important Features',
                 color_discrete_sequence=['rgb(56, 166, 165)'])
fig3_fl.update_layout(
    title=dict(font_size=20, x=0.5),
    xaxis=dict(title='Importance', title_font_size=18),
    yaxis=dict(title='Features', title_font_size=18),
    margin=dict(t=30, b=20, r=20),
    template=template
)

week = ['2021-11-2', '2021-11-9']
df2_fl = df_fl.loc[(df_fl.index > week[0]) & (df_fl.index < week[1])][['Actual', 'Prediction']]
fig4_fl = px.line(data_frame=df2_fl, x=df2_fl.index, y=['Actual', 'Prediction'], title='One Week of Data',
                  color_discrete_map={"Actual": 'rgb(29, 105, 150)', "Prediction": 'rgb(204, 80, 62)'})
fig4_fl.update_layout(title=dict(
    font_size=20, x=0.5),
    yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
    xaxis=dict(tickfont_size=13, title='Period', title_font_size=20),
    margin=dict(t=38, b=20),
    template=template)


def get_data_sql():
    conn = pymssql.connect(serverdb, username, password, database)
    cursor = conn.cursor()
    query = """SELECT TOP (72) *
            FROM dbo.future_data__FL
            ORDER BY [DATE] DESC"""
    df = pd.read_sql(query, conn)
    df.index = pd.to_datetime(df.Date)
    df = df.drop(['State', 'Date'], axis=1)
    df = df.sort_index()
    return df


FL_pred = get_data_sql()
FL_pred['pred'] = model.predict(FL_pred)
fig5_fl = px.line(data_frame=FL_pred, x=FL_pred.index, y='pred', title='Forecasting Demand in 3 Days',
                  color_discrete_sequence=['rgb(225, 124, 5)'])
fig5_fl.update_layout(title=dict(
    font_size=20, x=0.5),
    yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
    xaxis=dict(tickfont_size=13, title='Period', title_font_size=20),
    margin=dict(t=38, b=20),
    template=template)

sector_fl = pd.read_csv('../Data/FL/Florida_Sector_2020.csv', skiprows=4)
fig6_fl = px.pie(sector_fl, names='Category', values='Energy Consumption by End-Use Sector',
                 title='Energy Consumption by End-Use Sector(BTUs), 2020', color_discrete_sequence=px.colors.qualitative.Pastel,
                 category_orders={'Category':['Transportation','Residential','Industrial','Commercial'],})
fig6_fl.update_layout(title=dict(
    font_size=15, x=0.5),
    yaxis=dict(tickfont_size=13, title_font_size=15),
    xaxis=dict(tickfont_size=13, title_font_size=20, title='Thousand MegaWatt Hours'),
    margin=dict(t=33, b=25, r=40, l=50),
)
source_fl = pd.read_csv('../Data/FL/Florida_Net_Electricity_Generation.csv', skiprows=4)
fig7_fl = px.bar(source_fl, y='Category', x='Florida Net Electricity Generation thousand MWh', orientation='h', color_discrete_sequence=['rgb(237, 173, 8)'],
              title='Energy Generation by Source, Feb 2023')
fig7_fl.update_layout(title=dict(
    font_size=15, x=0.5),
    yaxis=dict(tickfont_size=13, title_font_size=15),
    xaxis=dict(tickfont_size=13, title_font_size=20, title='Thousand MegaWatt Hours'),
    margin=dict(t=33, b=25, r=20, l=30),)

layout = html.Div(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.H1('FLP'),
                    dcc.Markdown("""Florida Light and Power [(FLP)](https://www.fpl.com/about/company-profile.html) now
                     rebranded as [NextEra Energy](https://www.nexteraenergy.com/company.html) 
                    is the third largest eletric untilty company in the US. It provides power for over half of Florida.
                    They are a for profit company and is traded on the stock exchange under the ticker NEE.
                    """),
                    html.H2('Model Performance'),
                    dcc.Markdown("""The Root Mean Square Error (RMSE) and Mean Absolute Error (MAE) were 2029.25 and 
                    1464.15 respectively. The model preforms decently and but there are some weeks where the model
                    preforms extremely bad such as Jan 20, 2022 to Jan 31, 2022.
                      """),
                ], xs=12, sm=12, md=12, lg=11, xl=11, xxl=11,
            ),
        ],justify='around'),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='prediction_fl',
                              figure=create_scatter(), style={'width': '88vw', 'height': '40vh'})
                ], xs=12, sm=12, md=12, lg=11, xl=11, xxl=11,
            ),
        ],justify='around'),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='fi_fl',
                              figure=fig3_fl, style={'width': '38vw', 'height': '42vh'})
                ],
                xs=12, sm=12, md=3, lg=3, xl=3, xxl=3,

            ),
            dbc.Col(
                [
                    dcc.Graph(id='sector_fl',
                              figure=fig7_fl, style={'width': '30vw', 'height': '42vh'})
                ],
                xs=12, sm=12, md=8, lg=3, xl=3, xxl=3,
            ),
            dbc.Col(
                [
                    dcc.Graph(id='gen_fl',
                              figure=fig6_fl, style={'width': '24vw', 'height': '42vh'})
                ],
                xs=12, sm=12, md=8, lg=3, xl=3, xxl=3,
            )
        ], justify='around'),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Dropdown(id='freq_fl', multi=False, value='hour',
                                 options=[{'label': 'Hour', 'value': 'hour'},
                                          {'label': 'Month', 'value': 'month'},
                                          {'label': 'Day of the Week', 'value': 'days'},
                                          {'label': 'Quarter', 'value': 'quarter'},
                                          {'label': 'Day of Year', 'value': 'dayofyear'},
                                          ],
                                 style=dict(border='1px solid black', width='100%', )
                                 )

                ], xs=12, sm=12, md=10, lg=3, xl=3, xxl=3,
            ),
            dbc.Col(
                [
                    dcc.DatePickerSingle(id='cal_fl',
                                         clearable=False,
                                         persistence=True,
                                         month_format='MM-DD-YYYY',
                                         placeholder=' 11/02/2021',
                                         date=date(2021, 11, 9),
                                         with_portal=True,
                                         min_date_allowed=date(2021, 11, 2),
                                         max_date_allowed=date(2023, 4, 29),
                                         style=dict(border='2px solid black', width='68.5%', ), )
                ], xs=12, sm=12, md=10, lg=4, xl=4, xxl=4, className="text-center",
            ),
        ],justify='around' ,style={'align-items': 'center', 'display': 'flex', 'justify-content': 'center'}),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='freq_box_fl',
                              figure=fig1_fl, style={'width': '40vw', 'height': '40vh'})
                ], xs=12, sm=12, md=8, lg=4, xl=4, xxl=4,
            ),
            dbc.Col(
                [
                    dcc.Graph(id='week_fl',
                              figure=fig4_fl, style={'width': '45vw', 'height': '40vh'})
                ], xs=12, sm=12, md=8, lg=6, xl=6, xxl=6,
            ),
        ], justify='around'),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='future_fl',
                              figure=fig5_fl, style={'width': '88vw', 'height': '40vh'})
                ],
                xs=12, sm=12, md=12, lg=11, xl=11, xxl=11,
            )
        ], justify='around'),
    ])


@callback(
    Output('freq_box_fl', 'figure'),
    [Input('freq_fl', 'value')],
    [State("freq_fl", "options")],
)
def update_graph(value, opt):
    label = [x['label'] for x in opt if x['value'] == value]
    label = label[0]
    fig1_fl = px.box(df_fl, x=value, y='Actual', title=f'Range of Energy Demand by {label}',
                     color_discrete_sequence=['rgb(95, 70, 144)'])
    fig1_fl.update_layout(title=dict(
        font_size=20, x=0.5),
        yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
        xaxis=dict(tickfont_size=13, title=label, title_font_size=20),
        margin=dict(t=33, b=20, r=20),
        template=template
    )
    return fig1_fl


@callback(
    Output('week_fl', 'figure'),
    Input('cal_fl', 'date'),
)
def update_week(date_enter):
    aDate = datetime.datetime.strptime(date_enter, "%Y-%m-%d")
    oneWeek = datetime.timedelta(weeks=1)
    new_date = aDate + oneWeek
    fl2 = df_fl.loc[(df_fl.index > date_enter) & (df_fl.index < new_date)][['Actual', 'Prediction']]
    fig4fl = px.line(data_frame=fl2, x=fl2.index, y=['Actual', 'Prediction'], title='One Week of Data',
                   color_discrete_map={"Actual": 'rgb(29, 105, 150)', "Prediction": 'rgb(204, 80, 62)'})
    fig4fl.update_layout(title=dict(
        font_size=20, x=0.5),
        yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
        xaxis=dict(tickfont_size=13, title='Period', title_font_size=20),
        margin=dict(t=38, b=20),
        template=template)
    return fig4fl
