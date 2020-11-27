from bokeh.plotting import figure
from bokeh.models import ColorBar, ColumnDataSource
from bokeh.models import LinearColorMapper
from bokeh.transform import linear_cmap
from bokeh.palettes import magma
from bokeh.palettes import viridis
from bokeh.palettes import plasma
from bokeh.models.tools import HoverTool
from bokeh.core.properties import value
from bokeh.models import Legend
import pandas as pd
import math


def get_2_dim_plot_count(df, x_name, column, height, width):
    grouped_df = df.groupby([column, x_name])
    grouped_df = pd.DataFrame(grouped_df.size().reset_index(name="count"))

    legend_items = []

    unique_values = grouped_df[column].unique().tolist()
    p = figure(plot_width=width, plot_height=height)
    palette = viridis(len(unique_values))

    i = 0
    for val in unique_values:
        current = grouped_df[grouped_df[column] == val]
        r1 = p.line(current[x_name], current['count'], line_width=1, color=palette[i])
        r2 = p.circle(current[x_name], current['count'], fill_alpha=0.5, size=5, color=palette[i])
        legend_items.append((val, [r1, r2]))
        i = i + 1

    legend = Legend(items=legend_items, location=(0, -30))

    p.add_layout(legend, 'right')

    p.legend.click_policy = "hide"

    p.xaxis.axis_label = x_name
    p.yaxis.axis_label = 'count'

    return p


def get_2_dim_plot_sum(df, x_name, column, height, width, sort_col):
    cols_for_groups = [column, x_name, 'count']
    if sort_col != column:
        cols_for_groups.append(sort_col)
    grouped_df = df[cols_for_groups].groupby([column, x_name])

    if sort_col != column:
        grouped_df = pd.DataFrame(grouped_df.agg({sort_col: lambda x: x.iloc[0], 'count': 'sum'}).reset_index())
    else:
        grouped_df = pd.DataFrame(grouped_df.sum().reset_index())

    grouped_df = grouped_df.sort_values(by=[x_name, sort_col])

    legend_items = []

    unique_values = grouped_df[column].unique().tolist()
    p = figure(plot_width=width, plot_height=height)
    palette = viridis(len(unique_values))

    i = 0
    for val in unique_values:
        current = grouped_df[grouped_df[column] == val]
        r1 = p.line(current[x_name], current['count'], line_width=1, color=palette[i])
        r2 = p.circle(current[x_name], current['count'], fill_alpha=0.5, size=5, color=palette[i])
        legend_items.append((val, [r1, r2]))
        i = i + 1

    legend = Legend(items=legend_items, location=(0, -30))
    p.add_layout(legend, 'right')
    p.legend.click_policy = "hide"

    p.xaxis.axis_label = x_name
    p.yaxis.axis_label = 'Sum of events'

    return p


def get_bar_plot_count(df, column, title, height, width):
    grouped_df = df.groupby([column])
    grouped_df = pd.DataFrame(grouped_df.size().reset_index(name="count"))

    unique_values = grouped_df[column].unique().tolist()
    palette = viridis(len(unique_values))

    p = figure(x_range=unique_values, plot_height=height, plot_width=width, title=title)

    p.vbar(x=grouped_df[column], top=grouped_df['count'], width=0.9, color=palette, fill_alpha=.75)

    p.yaxis.axis_label = "Count"

    return p


def get_bar_plot_sum(df, column, title, height, width, sort_col):
    cols_for_groups = [column, 'count']
    if sort_col != column:
        cols_for_groups.append(sort_col)
    grouped_df = df[cols_for_groups].groupby([column])

    if sort_col != column:
        grouped_df = pd.DataFrame(grouped_df.agg({sort_col: lambda x: x.iloc[0], 'count': 'sum'}).reset_index())
    else:
        grouped_df = pd.DataFrame(grouped_df.sum().reset_index())

    grouped_df = grouped_df.sort_values(by=[sort_col])

    unique_values = grouped_df[column].unique().tolist()
    palette = viridis(len(unique_values))

    source = ColumnDataSource(data=dict(col=grouped_df[column], count=grouped_df['count'], color=palette))

    p = figure(x_range=unique_values, title=title, width=width, height=height)

    p.vbar(x='col', top='count', color='color', source=source, width=0.5, legend_field='col')

    p.xaxis.axis_label = ''
    p.yaxis.axis_label = 'Sum of events'

    p.xgrid.grid_line_color = None

    hover = HoverTool()
    hover.tooltips = [
        ("Type", '@col'),  # $name provides data from legend
        ("Value", '@count')  # @$name gives the value corresponding to the legend
    ]
    p.add_tools(hover)

    if len(unique_values) > 5:
        p.xaxis.major_label_orientation = math.pi / 2  # so that the labels do not come on top of each other

    new_legend = p.legend[0]
    # p.legend[0].plot = None
    p.add_layout(new_legend, 'right')
    p.legend.click_policy = "hide"

    return p
