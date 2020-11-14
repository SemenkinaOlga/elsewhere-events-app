import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from bokeh.embed import file_html
from bokeh.resources import CDN

import read_data as rd
import plots as plots

plot_height = 300
plot_width = 600


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    html.Iframe(
        srcDoc=html_bokeh,
        width=plot_width*1.1,
        height=plot_height*1.1
    ),

    html.Iframe(
        srcDoc=html_bokeh_2,
        width=plot_width*1.1,
        height=plot_height*1.1
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
