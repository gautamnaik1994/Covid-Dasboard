import json
import urllib.request
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

from components.html.Navbar import Navbar
from components.plots.DailyCovidLineChart import draw_line_chart
from components.plots.Barchart import draw_bar_chart
from components.plots.Piechart import draw_pie_chart
from components.plots.Heatmap import draw_heatmap
from helpers.apputils import date_to_utc

df_cases_time_series = []
df_statewise = []
df_statewise_daily = []

# df_raw = pd.read_json("https://api.covid19india.org/raw_data.json")


def get_clean_timeseries_data():
    # with open('./IndiaData/data.json') as json_file:
        # jsonData = json.load(json_file)
        # cases_time_series = jsonData["cases_time_series"]
        # statewise = jsonData["statewise"]
        # print(json.dumps(cases_time_series, indent=2))
    # df_cases_time_series = pd.DataFrame(data=cases_time_series)
    df_cases_time_series = pd.read_csv('./IndiaData/case_time_series.csv')
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
    df_statewise = pd.read_csv('./IndiaData/state_wise.csv')
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
    df_statewise_daily = pd.read_csv('./IndiaData/state_wise_daily.csv')
    df_statewise_daily = df_statewise_daily.drop(["TT"], axis=1)
    df_statewise_daily["Date"] = df_statewise_daily["Date"]+"20"
    df_statewise_daily["Date"] = pd.to_datetime(df_statewise_daily["Date"])
    return df_statewise_daily


df_cases_time_series = get_clean_timeseries_data()
df_statewise = get_clean_statewise_data()
df_statewise_daily = get_clean_statewise_daily_data()
# print(len(df_cases_time_series))

app = dash.Dash(__name__)

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
        children=html.Div(className="container-fluid", children=[
            html.Div(className="row", children=[
                html.Div(children=i, className="col") for i in [2, 5, 8, 8]
            ]),
            dcc.Graph(id="dailyGraph", figure=daily_data_figure),
            dcc.Store(id='clientside-daily_data_figure-store',
                      data=daily_data_figure,),
            dcc.RangeSlider(
                id='daily-range-slider',
                min=date_to_utc("01/01/2020"),
                max=date_to_utc("01/05/2020"),
                step=8.64e+7,
                value=[date_to_utc("01/01/2020"), date_to_utc("01/05/2020")]
            ),
            dcc.Graph(id="cumilativeGraph", figure=cumilative_data_figure),
            dcc.Store(id='clientside-cumilative_data_figure-store',
                      data=cumilative_data_figure,),
            dcc.RangeSlider(
                id='cumilative-range-slider',
                min=date_to_utc("01/01/2020"),
                max=date_to_utc("01/05/2020"),
                step=8.64e+7,
                value=[date_to_utc("01/01/2020"), date_to_utc("01/05/2020")]
            ),
            dcc.Graph(id="statewiseGraph",
                      figure=draw_bar_chart(df_statewise)),
            html.Div(className="row", children=[
                html.Div(className="col-12 col-md-6", children=[
                    dcc.Graph(id="statePieConfirmed",
                              figure=draw_pie_chart([df_statewise["State"],
                                                     df_statewise["Confirmed"]], name="Confirmed")),
                ]),
                html.Div(className="col-12 col-md-6", children=[

                    dcc.Graph(id="statePieActive",
                              figure=draw_pie_chart([df_statewise["State"],
                                                     df_statewise["Active"]], name="Active")),
                ]),
                html.Div(className="col-12 col-md-6", children=[
                    dcc.Graph(id="statePieRecovered",
                              figure=draw_pie_chart([df_statewise["State"],
                                                     df_statewise["Recovered"]],
                                                    name="Recovered")),
                ]),
                html.Div(className="col-12 col-md-6", children=[
                    dcc.Graph(id="statePieDeaths",
                              figure=draw_pie_chart([df_statewise["State"],
                                                     df_statewise["Deaths"]],
                                                    name="Deaths")),
                ]),
            ]),

            dcc.Graph(id="statewiseDailyConfirmed", figure=draw_heatmap(
                data=df_statewise_daily, data_type="Confirmed")),
            dcc.Graph(id="statewiseDailyRecovered", figure=draw_heatmap(
                data=df_statewise_daily, data_type="Recovered")),
            dcc.Graph(id="statewiseDailyDeceased",
                      figure=draw_heatmap(data=df_statewise_daily,
                                          data_type="Deceased")),

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


if __name__ == '__main__':
    app.run_server(debug=True)
