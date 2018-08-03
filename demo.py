
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash()


max_min_df = pd.read_csv('date_max_min.csv')


def generate_trace(the_month, line_type, show):
    """
    
    :param the_month:  the number of month
    :param line_type: liners or bar 
    :param show: max or min
    :return: 
    """
    result = []
    month_filter = max_min_df[max_min_df.month == the_month]
    for city in max_min_df.city_name.unique():
        city_filter = month_filter[month_filter.city_name == city]
        trace = dict(
            x=[x[1] for x in city_filter.date.items()],
            y=[x[1] for x in getattr(city_filter, show + "_num").items()],
            type=line_type,
            name=city
        )
        result.append(trace)
    return result

app.layout = html.Div(children=[

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='month-option-column',
                options=[{'label': str(i) + "月", 'value': i} for i in range(1, 13)],
                value=1
            ),
            dcc.RadioItems(
                id='line-options-column',
                options=[{'label': k, 'value': v} for k, v in {"折线图": "lines", "柱状图": "bar"}.items()],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='show-options-column',
                options=[{'label': k, 'value': v} for k, v in {"最高温度": "max", "最低温度": "min"}.items()],
                value='max'
            ),
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ]
        ),

    dcc.Graph(
        id='weather-month-graph',
    )
])


@app.callback(
    dash.dependencies.Output('weather-month-graph', 'figure'),
    [dash.dependencies.Input('month-option-column', 'value'),
     dash.dependencies.Input('line-options-column', 'value'),
     dash.dependencies.Input('show-options-column', 'value')])
def update_graph(the_month=None, line_type=None, show=None):
    return {
        'data': generate_trace(the_month, line_type, show),
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': "title"
            }],
            # 'yaxis': {'type': show},
            # 'xaxis': {'showgrid': False}
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
