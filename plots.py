from bokeh.plotting import figure
from bokeh.palettes import magma
from bokeh.palettes import viridis
from bokeh.palettes import plasma
from bokeh.models import Legend
import pandas as pd


def get_2_dim_plot_count(df, x_name, column, height, width):
    grouped_df = df.groupby([column, x_name])
    grouped_df = pd.DataFrame(grouped_df.size().reset_index(name="count"))

    legend_items = []

    unique_values = grouped_df[column].unique().tolist()
    p = figure(plot_width=width, plot_height=height)
    palette = viridis(len(unique_values))

    i = 0;
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


def get_2_dim_plot_sum(df, x_name, column, height, width):
    grouped_df = df.groupby([column, x_name])
    grouped_df = pd.DataFrame(grouped_df.sum().reset_index())

    legend_items = []

    unique_values = grouped_df[column].unique().tolist()
    p = figure(plot_width=width, plot_height=height)
    palette = viridis(len(unique_values))

    i = 0;
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
    p.yaxis.axis_label = 'Sum'

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


def get_bar_plot_sum(df, column, title, height, width):
    grouped_df = df.groupby([column])
    grouped_df = pd.DataFrame(grouped_df.sum().reset_index())

    unique_values = grouped_df[column].unique().tolist()
    palette = viridis(len(unique_values))

    p = figure(x_range=unique_values, plot_height=height, plot_width=width, title=title)

    p.vbar(x=grouped_df[column], top=grouped_df['count'], width=0.9, color=palette, fill_alpha=.75)

    p.yaxis.axis_label = "Sum"

    return p
