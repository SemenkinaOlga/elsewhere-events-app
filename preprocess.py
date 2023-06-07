import mapping
import clusterization

import numpy as np

import seaborn as sns


def get_palette(count):
    palette = list(sns.color_palette("viridis", count).as_hex())
    return palette


additional_columns = ['macro_region', 'meso_region', 'development_level', 'gdp_per_capita',
                      'gdp_volume', 'hdi', 'ECI', 'code', 'country_population_2018', 'country_population_2018_level']

default_colors = ['#440154', '#3f4687', '#248a8d', '#32b47a', '#fde725']
more_colors = ['#440154', '#3f4687', '#306a8e', '#248a8d', '#27a783', '#7bd150', '#fde725']
ten_colors = ['#440154', '#482878', '#3f4687', '#306a8e', '#248a8d',
              '#27a783', '#32b47a', '#7bd150', '#c2e02a', '#fde725']


def create_df_for_map(data, selected_year_min, selected_year_max, cluster_number, chosen_sources, use_clusters,
                      relative=True):
    column = 'count'
    if relative:
        column = 'relative_1M_count'
    df = data[data['year'] >= selected_year_min]
    df = df[df['year'] <= selected_year_max]
    df = df[df['source'].isin(chosen_sources)]
    df = df.reset_index()

    dict_cols = dict((col, lambda x: x.iloc[0]) for col in additional_columns if col in df.columns)
    dict_cols['count'] = "sum"
    dict_cols[column] = "sum"
    dict_cols['count'] = "sum"
    grouped_df = df.groupby(['country']).agg(dict_cols).reset_index()

    if use_clusters:
        df_predict = clusterization.clusterization_K_Means_1dim(grouped_df, 'country',
                                                                column, cluster_number)
        df_for_map = clusterization.add_indexation_by_events_amount_for_clusters(df_predict)

        return df_for_map
    else:
        return grouped_df


def create_df_for_bubble(data, chosen_sources):
    df = data[data['source'].isin(chosen_sources)]
    df = df.reset_index()

    dict_cols = dict((col, lambda x: x.iloc[0]) for col in additional_columns if col in df.columns)
    dict_cols['count'] = "sum"
    dict_cols['relative_1M_count'] = "sum"
    grouped_df = df.groupby(['country', 'year']).agg(dict_cols).reset_index()

    return grouped_df


def make_map(df_for_map, selected_year_min, selected_year_max, cluster_number, chosen_sources, use_clusters,
             relative=True):
    column = 'count'
    txt = "Relative events number "
    if relative:
        column = 'relative_1M_count'
        txt = "Events number "

    if use_clusters:
        name = txt + "for countries in [" + str(selected_year_min) + ", " + \
               str(selected_year_max) + "] - KMeans clusters " + str(cluster_number)
        return mapping.get_new_map(df_for_map, 'index', name, get_palette(cluster_number), True)
    else:
        name = txt + "per 1M people in [" + str(selected_year_min) + ", " + \
               str(selected_year_max) + "]"
        return mapping.get_new_map(df_for_map, column, name, get_palette(20))


def create_levels(df, column):
    min_value = df[column].min()
    max_value = df[column].max()

    steps_number = 10
    step = (max_value - min_value) / steps_number
    conditions = []
    choices = []

    current = min_value
    current_max = min_value + step

    divider = 1
    text = ''
    if max_value > 1000:
        if max_value > 1000000000:
            divider = 1000000000
            text = 'b'
        elif max_value > 1000000:
            divider = 1000000
            text = 'm'
        else:
            divider = 1000
            text = 'k'

    for i in range(0, steps_number):
        conditions.append((df[column] <= current_max) & (df[column] > current))
        choices.append(str(round(current / divider, 2)) + text + '-' + str(round(current_max / divider, 2)) + text)
        current = current + step
        if i == steps_number - 2:
            current_max = max_value
        else:
            current_max = current_max + step

    df[column + '_level'] = np.select(conditions, choices, default='unknown')

    return df
