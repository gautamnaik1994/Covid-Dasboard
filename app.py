import json
import urllib.request
from datetime import datetime, timedelta
from os import environ

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import requests
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv
from flask_assets import Bundle, Environment

from components.html.Navbar import Navbar
from components.html.Statbox import Statbox, StatboxBig
from components.plots.Barchart import draw_bar_chart
from components.plots.DailyCovidLineChart import draw_line_chart
from components.plots.Heatmap import draw_heatmap
from components.plots.Piechart import draw_pie_chart
from components.plots.Treemap import draw_treemap
from helpers.apputils import comma_number, convert_dateformat, date_to_utc

try:
    load_dotenv('.env')
except Exception as e:
    raise e
# print(environ.get('env'))

DEBUG = False

if environ.get('env') == 'dev':
    DEBUG = True
else:
    DEBUG = False


df_cases_time_series = []
df_statewise = []
df_statewise_daily = []
confirmed_world_rank = 0
zones=[]

# df_raw = pd.read_json("https://api.covid19india.org/raw_data.json")


def get_zones_data():
    data=[]
    if DEBUG:
        with open('./IndiaData/zones.json') as f:
            data=json.load(f)
    else:
        data=requests.get('https://api.covid19india.org/zones.json').json()

    df=pd.json_normalize(data["zones"])
    df_1 = df.rename(columns={'district':'id','statecode':'parent','zone':'value'})
    df_1["state"]=df["district"]
    df_1=df_1[["id","parent","value","state"]]
    df_2=df.groupby(["state","zone","statecode"]).count().reset_index().sort_values(["statecode","district"],ascending=False).groupby("statecode").first().reset_index()
    df_2=df_2.rename(columns={'statecode':'id','zone':'value'})
    df_2["parent"]="India"
    df_2=df_2[["id","parent","value","state"]]
    df_3=pd.DataFrame(data={'id':['India'],'parent':[""],'value':["White"],'state':["India"]})
    alldata=df_1.append(df_2).append(df_3)
    return alldata

def get_confirmed_world_rank():
    if DEBUG:
        cov_confirmed = pd.read_csv(
            "./IndiaData/time_series_covid19_confirmed_global.csv")
    else:
        cov_confirmed = pd.read_csv(
            "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    last_col = cov_confirmed.columns.values[-1]
    return cov_confirmed[["Country/Region", last_col]].groupby("Country/Region").sum().sort_values(by=last_col, ascending=False).index.get_loc("India")+1


def get_clean_timeseries_data():
    # with open('./IndiaData/data.json') as json_file:
        # jsonData = json.load(json_file)
        # cases_time_series = jsonData["cases_time_series"]
        # statewise = jsonData["statewise"]
        # print(json.dumps(cases_time_series, indent=2))
        # df_cases_time_series = pd.DataFrame(data=cases_time_series)
    if DEBUG:
        df_cases_time_series = pd.read_csv('./IndiaData/case_time_series.csv')
    else:
        df_cases_time_series = pd.read_csv(
            'https://api.covid19india.org/csv/latest/case_time_series.csv')
    df_cases_time_series["Date"] = df_cases_time_series["Date"] + " 2020"
    df_cases_time_series["Date"] = df_cases_time_series["Date"].apply(
        lambda x: datetime.strptime(x, "%d %B %Y"))
    df_cases_time_series = df_cases_time_series.set_index("Date")
    cols = df_cases_time_series.columns
    # print(cols)
    df_cases_time_series[cols] = df_cases_time_series[cols].apply(
        pd.to_numeric, errors='coerce')
    df_cases_time_series["Daily Active"] = df_cases_time_series["Daily Confirmed"] - \
        df_cases_time_series["Daily Deceased"] - \
        df_cases_time_series["Daily Recovered"]
    df_cases_time_series["Total Active"] = df_cases_time_series["Total Confirmed"] - \
        df_cases_time_series["Total Deceased"] - \
        df_cases_time_series["Total Recovered"]
    return df_cases_time_series


def get_clean_statewise_data():
    if DEBUG:
        df_statewise = pd.read_csv('./IndiaData/state_wise.csv')
    else:
        df_statewise = pd.read_csv(
            'https://api.covid19india.org/csv/latest/state_wise.csv')
    df_statewise = df_statewise.drop(
        ["Last_Updated_Time", "Delta_Confirmed", "Delta_Deaths", "Delta_Recovered"], axis=1)
    # cols = df_statewise.columns
    cols = ["Confirmed", "Recovered", "Deaths", "Active"]
    df_statewise[cols] = df_statewise[cols].apply(
        pd.to_numeric, errors='coerce')
    # print(df_statewise["State"])
    df_statewise = df_statewise[1:]
    return df_statewise


def get_clean_statewise_daily_data():
    if DEBUG:
        df_statewise_daily = pd.read_csv('./IndiaData/state_wise_daily.csv')
    else:
        df_statewise_daily = pd.read_csv(
            'https://api.covid19india.org/csv/latest/state_wise_daily.csv')
    df_statewise_daily = df_statewise_daily.drop(["TT"], axis=1)
    df_statewise_daily["Date"] = df_statewise_daily["Date"]+"20"
    df_statewise_daily["Date"] = pd.to_datetime(df_statewise_daily["Date"])
    return df_statewise_daily


df_cases_time_series = get_clean_timeseries_data()
df_statewise = get_clean_statewise_data()
df_statewise_daily = get_clean_statewise_daily_data()
confirmed_world_rank = get_confirmed_world_rank()
zones=get_zones_data()

# print(len(df_cases_time_series))

total_confirmed = df_cases_time_series["Total Confirmed"][-1]
total_recovered = df_cases_time_series["Total Recovered"][-1]
total_deceased = df_cases_time_series["Total Deceased"][-1]
today_confirmed = df_cases_time_series["Daily Confirmed"][-2:]
today_recovered = df_cases_time_series["Daily Recovered"][-2:]
today_deceased = df_cases_time_series["Daily Deceased"][-2:]


app = dash.Dash(__name__)
server = app.server
# assets.set_directory(".")
# assets.set_url(".")

app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
            <title>Covid</title>
            {%favicon%}
            {%css%}
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
'''

daily_data_figure = draw_line_chart(
    data=df_cases_time_series, graph_type="daily")
cumilative_data_figure = draw_line_chart(data=df_cases_time_series,
                                         graph_type="cumilative")

app.layout = html.Div([
    Navbar("Covid Dashboard"),
    html.Main(
        children=html.Div(className="container", children=[
            html.Div(className="row one-rem-mb", children=[

                html.Div(children=[
                    StatboxBig(name="Total Confirmed",
                               value=total_confirmed,
                               other_info={
                                   'New Cases': f'{ "▲" if today_confirmed[1] > today_confirmed[0] else "▼"}{today_confirmed[1]}', 'World Rank': confirmed_world_rank},
                               secondary_name="New Cases",
                               secondary_value=f'+{today_confirmed[0]}',
                               data=[df_cases_time_series[45:].index,
                                     df_cases_time_series["Daily Confirmed"][45:]],
                               color='confirmed',
                               ),
                ], className="col-12 col-lg-6 padding-top-15"),
                html.Div(children=[
                    Statbox(name="Total Active",
                            value=total_confirmed-total_deceased-total_recovered,
                            color="active",
                            secondary_name="New Cases",
                            secondary_value=[today_confirmed[0]-today_recovered[0]-today_deceased[0],
                                             today_confirmed[1]-today_recovered[1]-today_deceased[1]],
                            confirmed=total_confirmed,
                            className="one-rem-mb"),
                    Statbox(name="Total Recovered",
                            value=total_recovered,
                            color="recovered",
                            secondary_name="New Cases",
                            secondary_value=[
                                today_recovered[0], today_recovered[1]],
                            confirmed=total_confirmed,
                            className="one-rem-mb"),
                    Statbox(name="Total Deceased",
                            value=total_deceased,
                            color="death",
                            secondary_name="New Cases",
                            secondary_value=[
                                today_deceased[0], today_deceased[1]],
                            confirmed=total_confirmed
                            ),
                ], className="col-12 col-lg-6 padding-top-15"),
            ]),
            # html.Button('\U0001F447'),
            # html.Button('▲'),
            html.Div(className="card", children=[

                dcc.Graph(id="dailyGraph", figure=daily_data_figure),
                dcc.Store(id='clientside-daily_data_figure-store',
                          data=daily_data_figure,),
                dcc.RangeSlider(
                    id='daily-range-slider',
                    min=date_to_utc(
                        convert_dateformat(df_cases_time_series.index[0] -
                                           timedelta(days=2))),
                    max=date_to_utc(convert_dateformat(
                        df_cases_time_series.index[-1]+timedelta(days=10))),
                    step=8.64e+7,
                    value=[
                        date_to_utc(
                            convert_dateformat(df_cases_time_series.index[0] -
                                               timedelta(days=2))),
                        date_to_utc(convert_dateformat(
                            df_cases_time_series.index[-1]+timedelta(days=10))),
                    ]
                ),
            ]),
            dcc.Graph(id="cumilativeGraph", figure=cumilative_data_figure),
            dcc.Store(id='clientside-cumilative_data_figure-store',
                      data=cumilative_data_figure,),
            dcc.RangeSlider(
                id='cumilative-range-slider',
                min=date_to_utc(
                    convert_dateformat(df_cases_time_series.index[0] -
                                       timedelta(days=2))),
                max=date_to_utc(convert_dateformat(
                    df_cases_time_series.index[-1]+timedelta(days=10))),
                step=8.64e+7,
                value=[
                    date_to_utc(
                        convert_dateformat(df_cases_time_series.index[0] -
                                           timedelta(days=2))),
                    date_to_utc(convert_dateformat(
                        df_cases_time_series.index[-1]+timedelta(days=10))),
                ]
            ),
            dcc.Graph(figure=draw_bar_chart(df_statewise)),
            html.Div(className="row", children=[
                html.Div(className="col-12 col-lg-6", children=[
                    dcc.Graph(figure=draw_pie_chart(
                        [df_statewise["State"], df_statewise["Confirmed"]], name="Confirmed")),
                ]),
                html.Div(className="col-12 col-lg-6", children=[

                    dcc.Graph(figure=draw_pie_chart(
                        [df_statewise["State"], df_statewise["Active"]], name="Active")),
                ]),
                html.Div(className="col-12 col-lg-6", children=[
                    dcc.Graph(figure=draw_pie_chart(
                        [df_statewise["State"], df_statewise["Recovered"]], name="Recovered")),
                ]),
                html.Div(className="col-12 col-lg-6", children=[
                    dcc.Graph(figure=draw_pie_chart(
                        [df_statewise["State"], df_statewise["Deaths"]], name="Deaths")),
                ]),
            ]),
            dcc.Graph(figure=draw_heatmap(
                data=df_statewise_daily, data_type="Confirmed")),
            dcc.Graph(figure=draw_heatmap(
                data=df_statewise_daily, data_type="Recovered")),
            dcc.Graph(figure=draw_heatmap(
                data=df_statewise_daily, data_type="Deceased")),
            dcc.Graph(figure=draw_treemap( data=zones)),

        ])
    )
])

app.clientside_callback(
    """
    function(data, value) {
        return {
            ...data,
            'layout': {
                ...data["layout"],
                 'xaxis': {
                    'range':value,
                }
             }
        }
    }
    """,
    Output('dailyGraph', 'figure'),
    [Input('clientside-daily_data_figure-store', 'data'),
     Input('daily-range-slider', 'value')],
)

app.clientside_callback(
    """
    function(data, value) {
        return {
            ...data,
            'layout': {
                ...data["layout"],
                 'xaxis': {
                    'range':value,
                }
             }
        }
    }
    """,
    Output('cumilativeGraph', 'figure'),
    [Input('clientside-cumilative_data_figure-store', 'data'),
     Input('cumilative-range-slider', 'value')],
)

# if DEBUG == True:
# assets = Environment(server)
# assets.config['AUTOPREFIXER_BROWSERS'] = [
# '> 0.5%', 'last 3 versions', 'firefox 24', 'opera 12.1']
# scss = Bundle('scss/app.scss', filters='libsass', depends='**/*.scss')
# css = Bundle(scss, filters='autoprefixer6', output='../assets/style.css')
# css = Bundle(mid, filters='rcssmin', output='assets/style.css')
# assets.register('css', css)
# print(assets['css'].urls())

if __name__ == '__main__':
    app.run_server(debug=True)
