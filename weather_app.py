
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()


df = pd.read_csv('daily_weather.csv')

available_indicators = df['city_name'].unique()

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'curveNumber': 5, 'pointNumber': 6092,
                                   'pointIndex': 6092, 'x': 19, 'y': 22, 'text': '2018-06-19'}]}

        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-month--slider',
        min=df['month'].min(),
        max=df['month'].max(),
        value=df['month'].values,
        step=None,
        marks={str(month): str(month) for month in df['month'].unique()},
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-month--slider', 'value')])
def upmonth_figure(selected_month):
    filtered_df = df[df.month == selected_month]
    traces = []
    for i in filtered_df.city_name.unique():
        df_by_city_name = filtered_df[filtered_df['city_name'] == i]
        traces.append(go.Scatter(
            x=df_by_city_name['humidity'],
            y=df_by_city_name['temperature'],  # humidity
            text=df_by_city_name['date'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=str(i)
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': '湿度'},
            yaxis={'title': '温度', },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


def create_time_series(hoverData, date_key='temperature', title_key="天气"):
    # {'points': [{'curveNumber': 5, 'pointNumber': 6092, 'pointIndex': 6092, 'x': 19, 'y': 22, 'text': '2018-06-19'}]}
    _date = hoverData['text']
    data_frame = df[df.date == _date]

    city_name = data_frame.city_name.unique()[hoverData['curveNumber']]

    data_frame = data_frame[data_frame.city_name == city_name]
    title = "{city_name} {date} {title_key}详情".format(
        city_name=str(city_name), date=str(_date), title_key=title_key)
    return {
        'data': [go.Scatter(
            x=data_frame['hour'],
            y=data_frame[date_key],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData')])
def update_y_timeseries(hoverData):
    if hoverData:
        return create_time_series(hoverData["points"][0], 'humidity', "温度")


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData')])
def update_x_timeseries(hoverData):
    if hoverData:
        return create_time_series(hoverData["points"][0])


if __name__ == '__main__':
    app.run_server()
