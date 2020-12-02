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

dropdown_float_options = ['gdp_per_capita', 'gdp_volume', 'hdi', 'ECI']

# Read files
data = rd.read_data()
df_country = data['country']
df_country_year = data['country_year']
df_country_source_year = data['country_source_year']
df_city_year = data['city_year']
df_city = data['city']

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

fig_bokeh_bar = plots.get_bar_plot_sum(df_country_year, 'development_level', '', plot_height, plot_width, 'development_level')
html_bokeh_bar = file_html(fig_bokeh_bar, CDN, "fig_bokeh_bar")
fig_bokeh_plot = plots.get_2_dim_plot_sum(df_country_year, 'year', 'development_level', plot_height, plot_width, 'development_level')
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
    html.Div(id='graphs', children=[
        html.Div(id='graphs-settings', children=[
            html.Br(),
            html.Label('Color'),
            dcc.Dropdown(
                id='graphs-color',
                options=dropdown_options,
                value='development_level',
                clearable=False
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


@app.callback(
    Output('bokeh_bar', 'srcDoc'),
    Output('bokeh_plot', 'srcDoc'),
    [Input('graphs-color', 'value')])
def update(color):
    current_df = df_country_source_year
    n_color = color
    if color in dropdown_float_options:
        current_df = prep.create_levels(current_df, color)
        n_color = color + '_level'
    bokeh_bar = plots.get_bar_plot_sum(current_df, n_color, '', plot_height, plot_width, color)
    html_bar = file_html(bokeh_bar, CDN, "fig_bokeh_bar")
    bokeh_plot = plots.get_2_dim_plot_sum(current_df, 'year', n_color, plot_height, plot_width, color)
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
