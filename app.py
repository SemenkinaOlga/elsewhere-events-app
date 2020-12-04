import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from bokeh.embed import file_html
from bokeh.resources import CDN
import pandas as pd

import read_data as rd
import plots as plots
import preprocess as prep


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config["suppress_callback_exceptions"] = True

plot_height = 400
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

dropdown_color_schemes = [{'label': 'Plasma', 'value': 'Plasma'},
                          {'label': 'Viridis', 'value': 'Viridis'},
                          {'label': 'Inferno', 'value': 'Inferno'},
                          {'label': 'Turbo', 'value': 'Turbo'},
                          {'label': 'thermal', 'value': 'thermal'},
                          {'label': 'haline', 'value': 'haline'},
                          {'label': 'matter', 'value': 'matter'},
                          {'label': 'Sunset', 'value': 'Sunset'},
                          {'label': 'Agsunset', 'value': 'Agsunset'}]

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
                                         init_sources, init_use_clusters)
init_map = prep.make_map(init_df_for_map, min_year, max_year, init_cluster_number, init_sources, init_use_clusters)

init_map.save(rd.get_relative_path("init_map.html"))

init_col = 'development_level'

fig_bokeh_bar = plots.get_bar_plot_sum(df_country_year, init_col, '', plot_height, plot_width, init_col)
html_bokeh_bar = file_html(fig_bokeh_bar, CDN, "fig_bokeh_bar")
fig_bokeh_plot = plots.get_2_dim_plot_sum(df_country_year, 'year', init_col, plot_height, plot_width, init_col)
html_bokeh_plot = file_html(fig_bokeh_plot, CDN, "fig_bokeh_plot")

app.layout = html.Div(children=[
    html.H1(children='Elsewhere Events Dash'),
    html.Div(id='map-div', children=[
        html.Div(id='map-settings', children=[
            html.Br(),
            html.Div(id='chosen-year-label'),
            dcc.RangeSlider(
                id='year-range-slider',
                min=min_year,
                max=max_year,
                step=1,
                value=[min_year, max_year],
                marks={str(min_year): str(min_year),
                       str(max_year): str(max_year),
                       str(avg_year): str(avg_year)}
            ),
            html.Br(),
            dcc.Checklist(
                id='use-cluster-map',
                options=[
                    {'label': 'Use clusterization', 'value': 'UC'}
                ],
                value=['UC'],
                labelStyle={'display': 'inline-block'}
            ),
            html.Label('Clusters amount'),
            dcc.Slider(
                id='cluster-slider-map',
                min=min(clusters),
                max=max(clusters),
                value=init_cluster_number,
                marks={str(cl): str(cl) for cl in clusters},
                step=None
            ),
            html.Br(),
            html.Label('Sources'),
            dcc.Checklist(
                id='multi-source-map',
                options=[{'label': k, 'value': k} for k in sources],
                value=init_sources,
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '28%', 'float': 'left', 'display': 'inline-block'}),

        html.Div(id='main_map_div', children=[
            html.Iframe(
                id='map-main',
                style={'border': 'none', 'width': '100%', 'height': 600},
                srcDoc=open(rd.get_relative_path("init_map.html"), 'r').read()
            )
        ], style={'width': '68%', 'display': 'inline-block'})
    ]),
    html.Br(),
    html.Div(id='bubble-div', children=[
        html.Div(id='bubble-settings', children=[
            html.Label('X-axis'),
            dcc.Dropdown(
                id='bubble-x',
                options=dropdown_axis_options,
                value='gdp_per_capita',
                clearable=False
            ),
            html.Label('Y-axis'),
            dcc.Dropdown(
                id='bubble-y',
                options=dropdown_float_options,
                value='relative_1M_count',
                clearable=False
            ),
            html.Label('Bubble size'),
            dcc.Dropdown(
                id='bubble-size',
                options=dropdown_size_options,
                value='relative_1M_count',
                clearable=False
            ),
            html.Label('Color'),
            dcc.Dropdown(
                id='bubble-color',
                options=dropdown_all_options,
                value='macro_region',
                clearable=False
            ),
            html.Label('Color scheme'),
            dcc.Dropdown(
                id='bubble-color-scheme',
                options=dropdown_color_schemes,
                value='Viridis',
                clearable=False
            ),
            html.Br(),
            html.Label('Sources'),
            dcc.Checklist(
                id='bubble-sources',
                options=[{'label': k, 'value': k} for k in sources],
                value=init_sources,
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '28%', 'float': 'left', 'display': 'inline-block'}),
        html.Div(id='bubble-plot', children=[
            dcc.Graph(id='graph-bubble')
        ], style={'width': '68%', 'display': 'inline-block'})
    ]),
    html.Br(),
    html.Div(id='graphs', children=[
        html.Div(id='graphs-settings', children=[
            html.Br(),
            html.Label('Grouping by'),
            dcc.Dropdown(
                id='graphs-color',
                options=dropdown_options,
                value='development_level',
                clearable=False
            ),
            html.Br(),
            dcc.Checklist(
                id='use-trends',
                options=[
                    {'label': 'Use trends', 'value': 'UT'}
                ],
                value=[],
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '28%', 'float': 'left', 'display': 'inline-block'}),
        html.Div(id='graphs-plot', children=[
            html.Iframe(
                id="bokeh_bar",
                srcDoc=html_bokeh_bar,
                width=plot_width * 1.1,
                height=plot_height * 1.1
            ),
            html.Iframe(
                id="bokeh_plot",
                srcDoc=html_bokeh_plot,
                width=plot_width * 1.1,
                height=plot_height * 1.1
            )
        ], style={'width': '68%', 'display': 'inline-block'})

    ],
        style={'width': '100%', 'display': 'inline-block'}),
])

#
@app.callback(
    Output('graph-bubble', 'figure'),
    [Input('bubble-x', 'value'),
     Input('bubble-y', 'value'),
     Input('bubble-size', 'value'),
     Input('bubble-color', 'value'),
     Input('bubble-sources', 'value'),
     Input('bubble-color-scheme', 'value')])
def update_figure(x, y, size, color, chosen_sources, color_scheme):
    df_tmp = prep.create_df_for_bubble(df_country_source_year_extended, chosen_sources)
    # df_tmp = df_country_year_extended[df_country_year_extended['source'].isin(chosen_sources)]
    fig = plots.get_bubble_chart(df_tmp, x, y, size, color, color_scheme)
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('bokeh_bar', 'srcDoc'),
    Output('bokeh_plot', 'srcDoc'),
    [Input('graphs-color', 'value'),
     Input('use-trends', 'value')])
def update(color, use_trends):
    current_df = df_country_source_year
    n_color = color
    if color in dropdown_float_options:
        current_df = prep.create_levels(current_df, color)
        n_color = color + '_level'
    bokeh_bar = plots.get_bar_plot_sum(current_df, n_color, '', plot_height, plot_width, color)
    html_bar = file_html(bokeh_bar, CDN, "fig_bokeh_bar")
    bokeh_plot = plots.get_2_dim_plot_sum(current_df, 'year', n_color, plot_height, plot_width, color, use_trends)
    html_plot = file_html(bokeh_plot, CDN, "fig_bokeh_plot")
    return html_bar, html_plot


@app.callback(
    Output('map-main', 'srcDoc'),
    Output('chosen-year-label', 'children'),
    [Input('year-range-slider', 'value'),
     Input('cluster-slider-map', 'value'),
     Input('multi-source-map', 'value'),
     Input('use-cluster-map', 'value')])
def update(year_range, cluster_number, chosen_sources, use_clusters):
    df_for_map = prep.create_df_for_map(df_country_source_year, year_range[0], year_range[1], cluster_number, chosen_sources, use_clusters)
    current_map = prep.make_map(df_for_map, year_range[0], year_range[1], cluster_number, chosen_sources, use_clusters)
    current_map.save(rd.get_relative_path("map.html"))
    year_label = 'Year [' + str(year_range[0]) + ", " + str(year_range[1]) + "]"
    return open(rd.get_relative_path("map.html"), 'r').read(), year_label


if __name__ == '__main__':
    app.run_server(debug=True)
