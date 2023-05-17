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

template = pio.templates.default = "plotly"
import pickle
from datetime import date
import datetime
from flask_caching import Cache

dash.register_page(__name__,
                   path='/Texas',  # represents the url text
                   name='Texas',  # name of page, commonly used as name of link
                   title='Texas'  # epresents the title of browser's tab
                   )
app = dash.get_app()
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
TIMEOUT = 120

# page 2 data
df = pd.read_parquet('Data/TX/texas_df.parquet')
df.rename(columns={'value': 'Actual', 'prediction': 'Prediction'}, inplace=True)
fig1 = px.box(df, x='hour', y='Actual', title='Range of Energy Demand by Hour', )
fig1.update_layout(title=dict(
    font_size=20, x=0.55),
    yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts', title_font_size=15),
    xaxis=dict(tickfont_size=13, title_font_size=20, title='Hour'),
    margin=dict(t=33, b=20, r=20),
    template =template
)


@cache.memoize(timeout=TIMEOUT)
def create_scatter():
    fig2 = px.scatter(data_frame=df, x=df.index, y=['Actual', 'Prediction'],
                      opacity=.5, size_max=.2, render_mode='webgl', title='Actual VS Prediction')

    # Update the layout
    fig2.update_layout(
        title=dict(font_size=30),
        xaxis=dict(title='Period', title_font_size=25,tickfont_size=15,),
        yaxis=dict(title='Demand in Megawatt Hours', title_font_size=25, tickfont_size=15,),
        margin=dict(t=50, b=50,),
        template =template
    )
    return fig2


filename = R'Data\TX\model_TX.pkl'
with open(filename, 'rb') as f:
    model = pickle.load(f)
fi = pd.DataFrame(data=model.feature_importances_,
                  index=model.feature_name_,
                  columns=['importance'])
fi = fi.sort_values('importance', ascending=False)[:20]
fig3 = px.bar(fi, y=fi.index, x='importance', log_x=False, title='Top 20 Important Features')
fig3.update_layout(
        title=dict(font_size=20, x=0.8),
        xaxis=dict(title='Importance', title_font_size=18),
        yaxis=dict(title='Features', title_font_size=18),
        margin=dict(t=30, b=20, r=20),
        template =template
    )

week = ['2021-11-2', '2021-11-9']
df2 = df.loc[(df.index > week[0]) & (df.index < week[1])][['Actual', 'Prediction']]
fig4 = px.line(data_frame=df2, x=df2.index, y=['Actual', 'Prediction'], title='One Week of Data', markers=True)
fig4.update_layout(title=dict(
    font_size=20, x=0.45),
    yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
    xaxis=dict(tickfont_size=13, title='Period', title_font_size=20),
    margin=dict(t=38, b=20),
    template =template)

def get_data_sql():
    conn = pymssql.connect(serverdb,username, password, database)
    cursor = conn.cursor()
    query = """SELECT TOP (72) *
            FROM dbo.future_data__TX
            ORDER BY [DATE] DESC"""
    df = pd.read_sql(query, conn)
    df.index = pd.to_datetime(df.Date)
    df = df.drop(['State','Date'], axis=1)
    df = df.sort_index()
    return df

TX_pred = get_data_sql()
TX_pred['pred'] = model.predict(TX_pred)
fig5 = px.line(data_frame=TX_pred, x=TX_pred.index, y='pred',title='Predicting Demand in 3 Days')
fig5.update_layout(title=dict(
    font_size=20, x=0.45),
    yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
    xaxis=dict(tickfont_size=13, title='Period', title_font_size=20),
    margin=dict(t=38, b=20),
    template =template)


layout = html.Div(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.H1('ERCO'),
                    html.P('fdsfdfd'),
                    html.H2('Model Performance'),
                    html.P('MAE score, rsme'),
                ], width={'size': 9, 'offset': 1},
            ),
        ], ),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='prediction',
                              figure=create_scatter(), style={'width': '82vw', 'height': '60vh'})
                ], width={'size': 9, 'offset': 1},
            ),
        ], ),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Dropdown(id='freq', multi=False, value='hour',
                                 options=[{'label': 'Hour', 'value': 'hour'},
                                          {'label': 'Month', 'value': 'month'},
                                          {'label': 'Day of the Week', 'value': 'days'},
                                          {'label': 'Quarter', 'value': 'quarter'},
                                          {'label': 'Day of Year', 'value': 'dayofyear'},
                                          ],
                                 style=dict(border='1px solid black', width='100%',)
                                 )

                ], width={'size': 3, 'offset': 2},
            ),
            dbc.Col(
                [
                    dcc.DatePickerSingle(id='cal',
                                         clearable=False,
                                         persistence=True,
                                         month_format='MM-DD-YYYY',
                                         placeholder=' 11/02/2021',
                                         date=date(2021, 11, 9),
                                         with_portal=True,
                                         min_date_allowed=date(2021, 11, 2),
                                         max_date_allowed=date(2023, 4, 29),
                                         style=dict(border='2px solid black', width='68.5%', ),)
                ], width={'size': 3, 'offset': 3} ,className="text-center",
            ),
        ], style={'align-items': 'center', 'display': 'flex', 'justify-content': 'center'}),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='freq_box',
                              figure=fig1, style={'width': '40vw', 'height': '50vh'})
                ], width={'size': 5, 'offset': 1}
            ),
            dbc.Col(
                [
                    dcc.Graph(id='week',
                              figure=fig4, style={'width': '40vw', 'height': '50vh'})
                ], width={'size': 5, 'offset': 1}
            ),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id='fi',
                              figure=fig3, style={'width': '40vw', 'height': '50vh'})
                ], width={'size': 5, 'offset': 1}

            ),
            dbc.Col(
                [
                    dcc.Graph(id='future',
                              figure=fig5, style={'width': '40vw', 'height': '50vh'})
                ], width={'size': 5, 'offset': 1},
            )
        ]),
    ])


@callback(
    Output('freq_box', 'figure'),
    [Input('freq', 'value')],
    [State("freq", "options")],
)
def update_graph(value, opt):
    label = [x['label'] for x in opt if x['value'] == value]
    label = label[0]
    fig1 = px.box(df, x=value, y='Actual', title=f'Range of Energy Demand by {label}')
    fig1.update_layout(title=dict(
        font_size=20, x=0.55),
        yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
        xaxis=dict(tickfont_size=13, title=label, title_font_size=20),
        margin=dict(t=33, b=20, r=20),
        template =template
                    )
    return fig1


@callback(
    Output('week', 'figure'),
    Input('cal', 'date'),
)
def update_week(date_enter):
    aDate = datetime.datetime.strptime(date_enter, "%Y-%m-%d")
    oneWeek = datetime.timedelta(weeks=1)
    new_date = aDate + oneWeek
    tx2 = df.loc[(df.index > date_enter) & (df.index < new_date)][['Actual', 'Prediction']]
    fig4 = px.line(data_frame=tx2, x=tx2.index, y=['Actual', 'Prediction'], title='One Week of Data', markers=True)
    fig4.update_layout(title=dict(
        font_size=20, x=0.45),
        yaxis=dict(tickfont_size=13, title='Energy Demand in MegaWatts Hours', title_font_size=15),
        xaxis=dict(tickfont_size=13, title='Period', title_font_size=20),
        margin=dict(t=38, b=20),
        template =template)
    return fig4
