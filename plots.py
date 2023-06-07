import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

import seaborn as sns

dropdown_axis_x_options = {'gdp_per_capita': 'GDP per Capita',
                           'gdp_volume': 'GDP Volume',
                           'hdi': 'HDI',
                           'ECI': 'ECI',
                           'country_population_2018': 'Country Population 2018'}

dropdown_axis_y_options = {'gdp_per_capita': 'GDP per Capita',
                           'gdp_volume': 'GDP Volume',
                           'hdi': 'HDI',
                           'ECI': 'ECI',
                           'country_population_2018': 'Country Population 2018',
                           'count': 'Count',
                           'relative_1M_count': 'Relative per 1M count'}

dropdown_group_options = {'macro_region': 'Macro Region',
                          'meso_region': 'Meso Region',
                          'development_level': 'Development Level',
                          'country_population_2018_level': 'Country Population 2018 Level'}


def get_palette(count):
    palette = list(sns.color_palette("viridis", count).as_hex())
    return palette


def get_2_dim_plot_sum(df, y_name, x_name, column, sort_col, trends=False):
    cols_for_groups = [column, x_name, y_name]
    if sort_col != column:
        cols_for_groups.append(sort_col)
    grouped_df = df[cols_for_groups].groupby([column, x_name])

    if sort_col != column:
        grouped_df = pd.DataFrame(grouped_df.agg({sort_col: lambda x: x.iloc[0], y_name: 'sum'}).reset_index())
    else:
        grouped_df = pd.DataFrame(grouped_df.sum().reset_index())

    grouped_df = grouped_df.sort_values(by=[x_name, sort_col])

    unique_values = grouped_df[column].unique().tolist()

    fig = go.Figure()

    i = 0
    palette = get_palette(len(unique_values))
    for val in unique_values:
        current = grouped_df[grouped_df[column] == val]

        fig.add_traces(go.Scatter(x=current[x_name], y=current[y_name], mode='lines+markers', name=val,
                                  line=dict(color=palette[i], width=2)))

        if trends:
            x = [i for i in range(len(current[x_name]))]
            par = np.polyfit(x, current[y_name], 1, full=True)
            slope = par[0][0]
            intercept = par[0][1]
            y_predicted = [slope * i + intercept for i in x]

            fig.add_traces(go.Scatter(x=current[x_name], y=y_predicted, mode='lines+markers', name=val + " trends",
                                      line=dict(color=palette[i], width=2, dash='dash')))

        i = i + 1

    fig.update_layout(autosize=False, width=1000, height=350, showlegend=True, xaxis_title="Year",
                      yaxis_title="", template="plotly_white",
                      font=dict(family="Tahoma", size=12, color='black'))

    fig.update_xaxes(title='Year',
                     showline=True, linewidth=1, linecolor='black')
    fig.update_yaxes(title=dropdown_axis_y_options[y_name], showline=True, linewidth=1,
                     linecolor='black', gridcolor='lightgray')
    fig.update_traces(marker_line_color='black')

    return fig


def get_bar_plot_sum(df, y_name, column, sort_col):
    cols_for_groups = [column, y_name]
    if sort_col != column:
        cols_for_groups.append(sort_col)
    grouped_df = df[cols_for_groups].groupby([column])

    if sort_col != column:
        grouped_df = pd.DataFrame(grouped_df.agg({sort_col: lambda x: x.iloc[0], y_name: 'sum'}).reset_index())
    else:
        grouped_df = pd.DataFrame(grouped_df.sum().reset_index())

    if sort_col == 'country_population_2018_level':
        grouped_df = grouped_df.sort_values(by=['country_population_2018_level'],
                                            key=(lambda x: x.map(custom_dict)))
    else:
        grouped_df = grouped_df.sort_values(by=[sort_col])

    fig = px.bar(grouped_df, x=column, y=y_name, color=column, labels={'value': 'reliability'},
                 color_discrete_sequence=get_palette(len(grouped_df)), text_auto=True,
                 template="plotly_white")

    fig.update_layout(autosize=False, width=1000, height=350, showlegend=True,
                      template="plotly_white", font=dict(family="Tahoma", size=12, color='black'),
                      legend_title_text=dropdown_group_options[column])
    fig.update_xaxes(title='', showline=True, linewidth=1, linecolor='black')
    fig.update_yaxes(title=dropdown_axis_y_options[y_name], showline=True, linewidth=1,
                     linecolor='black', gridcolor='lightgray')

    return fig


custom_dict = {'<100k': 0, '100k-1M': 1, '1-5M': 3, '5-50M': 4, '50-100M': 5, '100-500M': 6, '>500M': 7}
pop_list = ['<100k', '100k-1M', '1-5M', '5-50M', '50-100M', '100-500M', '>500M']


def get_bubble_chart(df, x, y, size, color):
    min_x = min(df[x])
    max_x = max(df[x])
    min_y = min(df[y])
    max_y = max(df[y])
    df_tmp = df.sort_values('year')
    # df_tmp = df.sort_values(by=['year', 'country_population_2018_level'], key=(lambda x: x.map(custom_dict) if(x in pop_list) else x))
    palette = get_palette(len(df[color].unique()))

    plot = px.scatter(df_tmp, x=x, y=y, animation_frame="year", animation_group="country",
                      size=size, color=color, hover_name="country",
                      color_discrete_sequence=palette,
                      log_x=True, size_max=55, range_x=[min_x * 0.9, max_x * 1.1], range_y=[min_y * 0.9, max_y * 1.1]) \
        .update_layout(autosize=False, xaxis_title=dropdown_axis_x_options[x], yaxis_title=dropdown_axis_y_options[y],
                       width=1000, height=350, template="plotly_white",
                       font=dict(family="Tahoma", size=12, color='black'),
                       legend_title_text=dropdown_group_options[color])

    return plot
