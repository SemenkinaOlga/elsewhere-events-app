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
import clusterization
import mapping

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

plot_height = 300
plot_width = 600
default_colors = ['red', 'orange', 'lightyellow', 'green', 'darkgreen']
more_colors = ['red', 'orange', 'yellow', 'green', 'deepskyblue', 'blue', 'darkviolet']
ten_colors = ['red', 'orange', 'yellow', 'lime', 'green', 'deepskyblue', 'blue', 'indigo', 'deeppink', 'black']


def make_map(selected_year, cluster_number, sources, use_icons):
    df = df_country_year[df_country_year['year'] == selected_year]
    df_prediction = clusterization.clusterization_K_Means_1dim(df, 'country', 'relative_1M_count', cluster_number)

    name = "Relative events for countries in " + str(selected_year) + " - KMeans clusters " + str(cluster_number)

    df_for_map = clusterization.add_indexation_by_events_amount_for_clusters(df_prediction)

    if use_icons:
        return mapping.get_ico_map(df_for_map, 'index', name, ten_colors[:cluster_number], True)

    return mapping.get_simple_map(df_for_map, 'index', name, ten_colors[:cluster_number], True)


# Read files
data = rd.read_data()
df_country = data['country']
df_country_year = data['country_year']
df_country_source_year = data['country_source_year']
df_city_year = data['city_year']
df_city = data['city']

fig = px.bar(df_country, x="country", y="count", color="macro_region")
fig_bokeh = plots.get_bar_plot_sum(df_country_year, 'development_level', 'Title', plot_height, plot_width)
html_bokeh = file_html(fig_bokeh, CDN, "my plot")
fig_bokeh_2 = plots.get_2_dim_plot_sum(df_country_year, 'year', 'development_level', plot_height, plot_width)
html_bokeh_2 = file_html(fig_bokeh_2, CDN, "my plot")

years = df_country_year['year'].unique().tolist()
years.sort()
print(years)
min_year = min(years)
max_year = max(years)
clusters = [x for x in range(2, 13, 1)]
print(clusters)


init_cluster_number = 6
sources = df_country_source_year['source'].unique().tolist()
print(sources)
init_sources = ['TED', 'MEETUP', 'BEHANCE', 'EFLUX', 'ART_EDUCATION']
print(init_sources)
init_use_ico = False

init_map = make_map(max_year, init_cluster_number, init_sources, init_use_ico)
init_map.save(rd.get_relative_path("init_map.html"))

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

app.layout = html.Div(children=[
    html.H1(children='Elsewhere Events Dash'),
    html.Div(children='''A web application for research.'''),

    html.Div({
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            id='year-slider',
            min=2010,
            max=2020,
            value=2020,
            step=None
        )
    },
        style={'width': '100%', 'float': 'right', 'display': 'inline-block'}),

    html.Div({

    },
        style={'width': '100%', 'display': 'inline-block'}),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    html.Iframe(
        srcDoc=html_bokeh,
        width=plot_width * 1.1,
        height=plot_height * 1.1
    ),

    html.Iframe(
        srcDoc=html_bokeh_2,
        width=plot_width * 1.1,
        height=plot_height * 1.1
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
