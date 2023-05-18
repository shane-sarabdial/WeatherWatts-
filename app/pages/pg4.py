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
                   path='/florida',  # represents the url text
                   name='Florida',  # name of page, commonly used as name of link
                   title='Florida'  # epresents the title of browser's tab
                   )
app = dash.get_app()
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
TIMEOUT = 240

# page 2 data
df_fl = pd.read_parquet(r'app\Data\FL\FL_df.parquet')
df_fl.rename(columns={'value': 'Actual', 'prediction': 'Prediction'}, inplace=True)
fig1_fl = px.box(df_fl, x='hour', y='Actual', title='Range of Energy Demand by Hour',
                 color_discrete_sequence=['rgb(95, 70, 144)'])
fig1_fl.update_layout(title=dict(
    font_size=20, x=0.55),
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
        title=dict(font_size=30),
        xaxis=dict(title='Period', title_font_size=25, tickfont_size=15, ),
        yaxis=dict(title='Demand in Megawatt Hours', title_font_size=25, tickfont_size=15, ),
        margin=dict(t=50, b=50, ),
        template=template
    )
    return fig2_fl


filename = R'app\Data\FL\model_FL.pkl'
with open(filename, 'rb') as f:
    model = pickle.load(f)
fi_fl = pd.DataFrame(data=model.feature_importances_,
                     index=model.feature_name_,
                     columns=['importance'])
fi_fl = fi_fl.sort_values('importance', ascending=False)[:20]
fig3_fl = px.bar(fi_fl, y=fi_fl.index, x='importance', log_x=False, title='Top 20 Important Features',
                 color_discrete_sequence=['rgb(56, 166, 165)'])
fig3_fl.update_layout(
    title=dict(font_size=20, x=0.8),
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
    font_size=20, x=0.45),
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
fig5_fl = px.line(data_frame=FL_pred, x=FL_pred.index, y='pred', title='Predicting Demand in 3 Days',
                  color_discrete_sequence=['rgb(225, 124, 5)'])
fig5_fl.update_layout(title=dict(
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
                    dcc.Graph(id='prediction_fl',
                              figure=create_scatter(), style={'width': '82vw', 'height': '60vh'})
                ], width={'size': 9, 'offset': 1},
            ),
        ], ),
        html.Br(),
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

                ], width={'size': 3, 'offset': 2},
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
                ], width={'size': 3, 'offset': 3}, className="text-center",
            ),
        ], style={'align-items': 'center', 'display': 'flex', 'justify-content': 'center'}),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='freq_box_fl',
                              figure=fig1_fl, style={'width': '40vw', 'height': '50vh'})
                ], width={'size': 5, 'offset': 1}
            ),
            dbc.Col(
                [
                    dcc.Graph(id='week_fl',
                              figure=fig4_fl, style={'width': '40vw', 'height': '50vh'})
                ], width={'size': 5, 'offset': 1}
            ),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='fi_fl',
                              figure=fig3_fl, style={'width': '40vw', 'height': '50vh'})
                ], width={'size': 5, 'offset': 1}

            ),
            dbc.Col(
                [
                    dcc.Graph(id='future_fl',
                              figure=fig5_fl, style={'width': '40vw', 'height': '50vh'})
                ], width={'size': 5, 'offset': 1},
            )
        ]),
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
        font_size=20, x=0.55),
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
        font_size=20, x=0.45),
        yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
        xaxis=dict(tickfont_size=13, title='Period', title_font_size=20),
        margin=dict(t=38, b=20),
        template=template)
    return fig4fl
