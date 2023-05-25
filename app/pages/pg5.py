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
                   path='/california',  # represents the url text
                   name='California',  # name of page, commonly used as name of link
                   title='California',  # epresents the title of browser's tab
                   order=1
                   )
app = dash.get_app()
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
TIMEOUT = 240

# page 2 data
df_ca = pd.read_parquet('../Data/CA/CA_df.parquet')
df_ca.rename(columns={'value': 'Actual', 'prediction': 'Prediction'}, inplace=True)
fig1_ca = px.box(df_ca, x='hour', y='Actual', title='Range of Energy Demand by Hour',
                 color_discrete_sequence=['rgb(95, 70, 144)'])
fig1_ca.update_layout(title=dict(
    font_size=20, x=0.5),
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
        title=dict(font_size=30, x=0.5),
        xaxis=dict(title='Period', title_font_size=25, tickfont_size=15, ),
        yaxis=dict(title='Demand in Megawatt Hours', title_font_size=20, tickfont_size=15, ),
        margin=dict(t=50, b=50, ),
        template=template
    )
    return fig2_ca


filename = '../Data/CA/model_CA.pkl'
with open(filename, 'rb') as f:
    model = pickle.load(f)
fi_ca = pd.DataFrame(data=model.feature_importances_,
                     index=model.feature_name_,
                     columns=['importance'])
fi_ca = fi_ca.sort_values('importance', ascending=False)[:20]
fig3_ca = px.bar(fi_ca, y=fi_ca.index, x='importance', log_x=False, title='Top 20 Important Features',
                 color_discrete_sequence=['rgb(56, 166, 165)'])
fig3_ca.update_layout(
    title=dict(font_size=20, x=0.5),
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
    font_size=20, x=0.5),
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
fig5_ca = px.line(data_frame=CA_pred, x=CA_pred.index, y='pred', title='Forecasting Demand in 3 Days',
                  color_discrete_sequence=['rgb(225, 124, 5)'])
fig5_ca.update_layout(title=dict(
    font_size=20, x=0.5),
    yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
    xaxis=dict(tickfont_size=13, title='Period', title_font_size=20),
    margin=dict(t=38, b=20),
    template=template)

sector_ca = pd.read_csv('../Data/CA/California_Sector_2020.csv', skiprows=4)
fig6_ca = px.pie(sector_ca, names='Category', values='Energy Consumption by End-Use Sector',
                 title='Energy Consumption by End-Use Sector(BTUs), 2020', color_discrete_sequence=px.colors.qualitative.Pastel,
                 category_orders={'Category':['Transportation','Residential','Industrial','Commercial'],})
fig6_ca.update_layout(title=dict(
    font_size=15, x=0.5),
    yaxis=dict(tickfont_size=13, title_font_size=15),
    xaxis=dict(tickfont_size=13, title_font_size=20, title='Hour'),
    margin=dict(t=33, b=25, r=40, l=50),
)
source_ca = pd.read_csv('../Data/CA/California_Net_Electricity_Generation.csv', skiprows=4)
fig7_ca = px.bar(source_ca, y='Category', x='California Net Electricity Generation thousand MWh', orientation='h', color_discrete_sequence=['rgb(237, 173, 8)'],
              title='Energy Generation by Source, Feb 2023')
fig7_ca.update_layout(title=dict(
    font_size=15, x=0.5),
    yaxis=dict(tickfont_size=13, title_font_size=15),
    xaxis=dict(tickfont_size=13, title_font_size=20, title='Thousand MegaWatt Hours'),
    margin=dict(t=33, b=25, r=20, l=30),)


layout = html.Div(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.H1('CAISO'),
                    dcc.Markdown("""The California Independent System Operator 
                    [(CAISO)](https://www.caiso.com/about/Pages/default.aspx) is an ISO that supplies power to about 
                    80% of the states population and deliver 300 million megawatt hours to its residents. Their focus is 
                    on creating renewable and sustainable energy. In 2018, California ranked first in the nations
                    as a producer of electricity from solar, geothermal and biomass resources."""),
                    html.H2('Model Performance'),
                    dcc.Markdown("""The Root Mean Square Error (RMSE) and Mean Absolute Error (MAE) were 1721.98 and 
                    1220.40 respectively. The model preforms well but under predicts during the summer months. The 
                    adjust close energy lags are higher on the feature importance list than the other models, this 
                    may suggest California is more sensitive to energy price fluctuations. 
                      """),
                ], xs=12, sm=12, md=12, lg=11, xl=11, xxl=11,
            ),
        ],justify='around' ),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='prediction_ca',
                              figure=create_scatter(), style={'width': '88vw', 'height': '40vh'})
                ], xs=12, sm=12, md=12, lg=11, xl=11, xxl=11,
            ),
        ],justify='around'),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='fi_ca',
                              figure=fig3_ca, style={'width': '38vw', 'height': '42vh'})
                ],
                xs=12, sm=12, md=3, lg=3, xl=3, xxl=3,

            ),
            dbc.Col(
                [
                    dcc.Graph(id='sector_ca',
                              figure=fig7_ca, style={'width': '30vw', 'height': '42vh'})
                ],
                # width={'size': 5, 'offset': 1},
                xs=12, sm=12, md=8, lg=3, xl=3, xxl=3,
            ),
            dbc.Col(
                [
                    dcc.Graph(id='gen_ca',
                              figure=fig6_ca, style={'width': '24vw', 'height': '42vh'})
                ],
                xs=12, sm=12, md=8, lg=3, xl=3, xxl=3,
            )
        ], justify='around'),
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

                ], xs=12, sm=12, md=10, lg=3, xl=3, xxl=3,
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
                ], xs=12, sm=12, md=10, lg=4, xl=4, xxl=4, className="text-center",
            ),
        ],justify='around', style={'align-items': 'center', 'display': 'flex', 'justify-content': 'center'}),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='freq_box_ca',
                              figure=fig1_ca, style={'width': '40vw', 'height': '40vh'})
                ], xs=12, sm=12, md=8, lg=4, xl=4, xxl=4,
            ),
            dbc.Col(
                [
                    dcc.Graph(id='week_ca',
                              figure=fig4_ca, style={'width': '45vw', 'height': '40vh'})
                ], xs=12, sm=12, md=8, lg=6, xl=6, xxl=6,
            ),
        ], justify='around'),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='future_ca',
                              figure=fig5_ca, style={'width': '88vw', 'height': '40vh'})
                ],
                xs=12, sm=12, md=12, lg=11, xl=11, xxl=11,
            )
        ], justify='around'),
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
        font_size=20, x=0.5),
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
        font_size=20, x=0.5),
        yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
        xaxis=dict(tickfont_size=13, title='Period', title_font_size=20),
        margin=dict(t=38, b=20),
        template=template)
    return fig4_ca
