import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import read_data as rd
import plots as plots
import preprocess as prep
import regression as regr

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config["suppress_callback_exceptions"] = True

plot_height = 350
plot_width = 900

dropdown_options = [{'label': 'Macro Region', 'value': 'macro_region'},
                    {'label': 'Meso Region', 'value': 'meso_region'},
                    {'label': 'Development Level', 'value': 'development_level'},
                    {'label': 'GDP per Capita', 'value': 'gdp_per_capita'},
                    {'label': 'GDP Volume', 'value': 'gdp_volume'},
                    {'label': 'HDI', 'value': 'hdi'},
                    {'label': 'ECI', 'value': 'ECI'},
                    {'label': 'Country Population 2018 Level', 'value': 'country_population_2018_level'},
                    {'label': 'Source', 'value': 'source'}]

dropdown_all_options = [{'label': 'Macro Region', 'value': 'macro_region'},
                        {'label': 'Meso Region', 'value': 'meso_region'},
                        {'label': 'Development Level', 'value': 'development_level'},
                        {'label': 'GDP per Capita', 'value': 'gdp_per_capita'},
                        {'label': 'GDP Volume', 'value': 'gdp_volume'},
                        {'label': 'HDI', 'value': 'hdi'},
                        {'label': 'ECI', 'value': 'ECI'},
                        {'label': 'Country Population 2018 Level', 'value': 'country_population_2018_level'},
                        {'label': 'Country Population 2018', 'value': 'country_population_2018'},
                        {'label': 'Count', 'value': 'count'},
                        {'label': 'Relative per 1M count', 'value': 'relative_1M_count'}]

dropdown_grouping_options = [{'label': 'Macro Region', 'value': 'macro_region'},
                             {'label': 'Meso Region', 'value': 'meso_region'},
                             {'label': 'Development Level', 'value': 'development_level'},
                             {'label': 'Country Population 2018 Level', 'value': 'country_population_2018_level'}]

dropdown_float_options = [{'label': 'GDP per Capita', 'value': 'gdp_per_capita'},
                          {'label': 'GDP Volume', 'value': 'gdp_volume'},
                          {'label': 'HDI', 'value': 'hdi'},
                          {'label': 'ECI', 'value': 'ECI'},
                          {'label': 'Country Population 2018', 'value': 'country_population_2018'},
                          {'label': 'Count', 'value': 'count'},
                          {'label': 'Relative per 1M count', 'value': 'relative_1M_count'}]

dropdown_size_options = [{'label': 'Country Population 2018', 'value': 'country_population_2018'},
                         {'label': 'Count', 'value': 'count'},
                         {'label': 'Relative per 1M count', 'value': 'relative_1M_count'}]

dropdown_axis_options = [{'label': 'GDP per Capita', 'value': 'gdp_per_capita'},
                         {'label': 'GDP Volume', 'value': 'gdp_volume'},
                         {'label': 'HDI', 'value': 'hdi'},
                         {'label': 'ECI', 'value': 'ECI'},
                         {'label': 'Country Population 2018', 'value': 'country_population_2018'}]

dropdown_y_axes_options = [{'label': 'Count', 'value': 'count'},
                           {'label': 'Relative per 1M count', 'value': 'relative_1M_count'}]

dropdown_count_options = [{'label': 'Count', 'value': 'count'},
                          {'label': 'Relative per 1M count', 'value': 'relative_1M_count'}]

# Read files
data = rd.read_data()
df_country = data['country']
df_country_year = data['country_year']
df_country_source_year = data['country_source_year']
df_city_year = data['city_year']
df_city = data['city']
df_country_year_extended = data['country_year_extended']
df_country_source_year_extended = data['country_source_year_extended']

years = df_country_source_year['year'].unique().tolist()
years.sort()
min_year = min(years)
max_year = max(years)
avg_year = min_year + round((max_year - min_year) / 2.0)
clusters = [x for x in range(2, 13, 1)]
init_cluster_number = 6
init_use_clusters = True
sources = df_country_source_year['source'].unique().tolist()
init_sources = ['TED', 'MEETUP', 'BEHANCE', 'EFLUX', 'ART_EDUCATION']
init_use_ico = False

init_df_for_map = prep.create_df_for_map(df_country_source_year, min_year, max_year, init_cluster_number,
                                         init_sources, init_use_clusters, True)
init_map = prep.make_map(init_df_for_map, min_year, max_year, init_cluster_number, init_sources,
                         init_use_clusters, True)
init_map.save(rd.get_relative_path("init_map.html"))

city_map_count = open(rd.get_relative_path("map_city_count.html"), 'r').read()
city_map_relative = open(rd.get_relative_path("map_city_relative.html"), 'r').read()

init_col = 'development_level'

app.layout = html.Div(children=[
    html.H2(children='Elsewhere Events Dash', style={'textAlign': 'center'}),
    html.Div(id='map-div', children=[
        html.Div(id='map-settings', children=[
            html.H4(children='Maps settings', style={'textAlign': 'center'}),
            dcc.RangeSlider(
                id='year-range-slider',
                min=min_year,
                max=max_year,
                step=1,
                value=[min_year, max_year],
                marks={str(min_year): str(min_year),
                       str(max_year): str(max_year),
                       str(avg_year): str(avg_year)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            dcc.Checklist(
                id='use-cluster-map',
                options=[
                    {'label': 'Use clusterization', 'value': 'UC'}
                ],
                value=['UC'],
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Slider(
                id='cluster-slider-map',
                min=min(clusters),
                max=max(clusters),
                value=init_cluster_number,
                marks={str(cl): str(cl) for cl in clusters},
                step=None
            ),
            html.Label('Value'),
            dcc.Dropdown(
                id='city-color',
                options=[{'label': 'Events count', 'value': 'count'},
                         {'label': 'Relative per 1M events count', 'value': 'relative_1M_count'}],
                value='relative_1M_count',
                clearable=False
            ),
            html.Label('Sources'),
            dcc.Checklist(
                id='multi-source-map',
                options=[{'label': k, 'value': k} for k in sources],
                value=init_sources,
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '19%', 'float': 'left', 'display': 'inline-block', 'height': 280}),
        html.Div(id='city-div-tmp-2', children=[
        ], style={'width': '1%', 'display': 'inline-block', 'height': 280}),
        html.Div(id='main_map_div', children=[
            html.H4(children='Events by country', style={'textAlign': 'center'}),
            html.Iframe(
                id='map-main',
                style={'border': 'none', 'width': '100%', 'height': 280},
                srcDoc=open(rd.get_relative_path("init_map.html"), 'r').read()
            )
        ], style={'width': '38%', 'display': 'inline-block', 'height': 280}),
        html.Div(id='city-div-tmp', children=[
        ], style={'width': '1%', 'display': 'inline-block', 'height': 280}),
        html.Div(id='city-div', children=[
            html.H4(children='Events by cities', style={'textAlign': 'center'}),
            html.Div(id='city-main', children=[
                html.Iframe(
                    id='city-map',
                    style={'border': 'none', 'width': '100%', 'height': 280},
                    srcDoc=city_map_relative
                )
            ], style={'width': '100%', 'display': 'inline-block', 'height': 280}),
        ], style={'width': '38%', 'display': 'inline-block', 'height': 280}),
    ]),

    html.Div(id='bubble-div', children=[
        html.Div(id='bubble-settings', children=[
            html.H4(children='Plot settings', style={'textAlign': 'center'}),
            dcc.RadioItems(id='plot_type_radio', options=['Bubbles', 'Bar', 'Trends', 'Regression'],
                           value='Regression', labelStyle={'display': 'inline-block'}),
            html.P(id="x_axis_text", children=["X-axis"], style={'display': 'none'}),
            dcc.Dropdown(
                id='x_axis',
                options=dropdown_axis_options,
                value='gdp_per_capita',
                clearable=False
            ),
            html.Label('Y-axis'),
            dcc.Dropdown(
                id='y_axis',
                options=dropdown_y_axes_options,
                value='relative_1M_count',
                clearable=False
            ),
            html.P(id="grouping_text", children=["Grouping by (color)"], style={'display': 'none'}),
            dcc.Dropdown(
                id='graphs-color',
                options=dropdown_grouping_options,
                value='development_level',
                clearable=False
            ),
            dcc.Checklist(
                id='use-trends',
                options=[
                    {'label': 'Use trends', 'value': 'UT'}
                ],
                value=['UT'],
                labelStyle={'display': 'inline-block'}
            ),
            html.P(id="bubble_size_text", children=["Bubble size"],
                   style={'display': 'none'}),
            dcc.Dropdown(
                id='bubble-size',
                options=dropdown_size_options,
                value='relative_1M_count',
                clearable=False
            )
        ], style={'width': '28%', 'float': 'left', 'display': 'inline-block'}),
        html.Div(id='bubble-plot', children=[
            dcc.Graph(id='graph-bubble'),
            dcc.Graph(id='regression-plot'),
            dcc.Graph(id='graph-bar'),
            dcc.Graph(id='graph-trends')
        ], style={'width': '68%', 'display': 'inline-block', 'height': 350})
    ])
])


@app.callback(
    Output('city-map', 'srcDoc'),
    [Input('city-color', 'value')])
def update(color):
    if color == 'count':
        return city_map_count
    else:
        return city_map_relative


@app.callback(
    Output(component_id='x_axis_text', component_property='style'),
    Output(component_id='x_axis', component_property='style'),
    [Input(component_id='plot_type_radio', component_property='value')])
def show_hide_element(plot_type):
    # ['Bubbles', 'Bar', 'Trends', 'Regression']
    if plot_type == 'Bubbles' or plot_type == 'Regression':
        return {'display': 'block'}, {'display': 'block'}
    return {'display': 'none'}, {'display': 'none'}


@app.callback(
    Output(component_id='grouping_text', component_property='style'),
    Output(component_id='graphs-color', component_property='style'),
    [Input(component_id='plot_type_radio', component_property='value')])
def show_hide_element(plot_type):
    # ['Bubbles', 'Bar', 'Trends', 'Regression']
    if plot_type == 'Regression':
        return {'display': 'none'}, {'display': 'none'}
    return {'display': 'block'}, {'display': 'block'}


@app.callback(
    Output(component_id='bubble_size_text', component_property='style'),
    Output(component_id='bubble-size', component_property='style'),
    Output(component_id='graph-bubble', component_property='style'),
    [Input(component_id='plot_type_radio', component_property='value')])
def show_hide_element(plot_type):
    # ['Bubbles', 'Bar', 'Trends', 'Regression']
    if plot_type == 'Bubbles':
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@app.callback(
    Output(component_id='graph-bar', component_property='style'),
    [Input(component_id='plot_type_radio', component_property='value')])
def show_hide_element(plot_type):
    # ['Bubbles', 'Bar', 'Trends', 'Regression']
    if plot_type == 'Bar':
        return {'display': 'block'}
    return {'display': 'none'}


@app.callback(
    Output(component_id='graph-trends', component_property='style'),
    Output(component_id='use-trends', component_property='style'),
    [Input(component_id='plot_type_radio', component_property='value')])
def show_hide_element(plot_type):
    # ['Bubbles', 'Bar', 'Trends', 'Regression']
    if plot_type == 'Trends':
        return {'display': 'block'}, {'display': 'block'}
    return {'display': 'none'}, {'display': 'none'}


@app.callback(
    Output(component_id='regression-plot', component_property='style'),
    [Input(component_id='plot_type_radio', component_property='value')])
def show_hide_element(plot_type):
    # ['Bubbles', 'Bar', 'Trends', 'Regression']
    if plot_type == 'Regression':
        return {'display': 'block'}
    return {'display': 'none'}

@app.callback(
    Output('graph-bubble', 'figure'),
    [Input('x_axis', 'value'),
     Input('y_axis', 'value'),
     Input('bubble-size', 'value'),
     Input('graphs-color', 'value'),
     Input('multi-source-map', 'value')])
def update(x, y, size, color, chosen_sources):
    df_tmp = prep.create_df_for_bubble(df_country_source_year_extended, chosen_sources)
    fig = plots.get_bubble_chart(df_tmp, x, y, size, color)
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('graph-bar', 'figure'),
    Output('graph-trends', 'figure'),
    [Input('graphs-color', 'value'),
     Input('y_axis', 'value'),
     Input('use-trends', 'value')])
def update(color, y, use_trends):
    current_df = df_country_source_year
    n_color = color
    if color in dropdown_float_options:
        current_df = prep.create_levels(current_df, color)
        n_color = color + '_level'
    bar = plots.get_bar_plot_sum(current_df, y, n_color, color)
    plot = plots.get_2_dim_plot_sum(current_df, y, 'year', n_color, color, use_trends)
    return bar, plot


@app.callback(
    Output('map-main', 'srcDoc'),
    [Input('year-range-slider', 'value'),
     Input('cluster-slider-map', 'value'),
     Input('multi-source-map', 'value'),
     Input('use-cluster-map', 'value'),
     Input('city-color', 'value')])
def update(year_range, cluster_number, chosen_sources, use_clusters, column):
    relative = False
    if column == 'relative_1M_count':
        relative = True
    df_for_map = prep.create_df_for_map(df_country_source_year, year_range[0], year_range[1], cluster_number,
                                        chosen_sources, use_clusters, relative)
    current_map = prep.make_map(df_for_map, year_range[0], year_range[1], cluster_number, chosen_sources,
                                use_clusters, relative)
    current_map.save(rd.get_relative_path("map.html"))
    return open(rd.get_relative_path("map.html"), 'r').read()


@app.callback(
    Output('regression-plot', 'figure'),
    [Input('x_axis', 'value'),
     Input('y_axis', 'value')])
def update(field, value):
    res = regr.linear_regression(df_country, field, value)
    return res


if __name__ == '__main__':
    app.run(debug=True)
