import mapping
import clusterization

import numpy as np


additional_columns = ['macro_region', 'meso_region', 'development_level', 'gdp_per_capita',
                      'gdp_volume', 'hdi', 'ECI', 'code', 'country_population_2018', 'country_population_2018_level']

default_colors = ['red', 'orange', 'lightyellow', 'green', 'darkgreen']
more_colors = ['red', 'orange', 'yellow', 'green', 'deepskyblue', 'blue', 'darkviolet']
ten_colors = ['red', 'orange', 'yellow', 'lime', 'green', 'deepskyblue', 'blue', 'indigo', 'deeppink', 'black']


def create_df_for_map(data, selected_year_min, selected_year_max, cluster_number, chosen_sources, use_clusters):
    df = data[data['year'] >= selected_year_min]
    df = df[df['year'] <= selected_year_max]
    df = df[df['source'].isin(chosen_sources)]
    df = df.reset_index()

    dict_cols = dict((col, lambda x: x.iloc[0]) for col in additional_columns if col in df.columns)
    dict_cols['count'] = "sum"
    dict_cols['relative_1M_count'] = "sum"
    grouped_df = df.groupby(['country']).agg(dict_cols).reset_index()

    if use_clusters:
        df_predict = clusterization.clusterization_K_Means_1dim(grouped_df, 'country',
                                                                'relative_1M_count', cluster_number)
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


def make_map(df_for_map, selected_year_min, selected_year_max, cluster_number, chosen_sources, use_clusters):
    if use_clusters:
        name = "Relative events for countries in [" + str(selected_year_min) + ", " + \
               str(selected_year_max) + "] - KMeans clusters " + str(cluster_number)
        return mapping.get_new_map(df_for_map, 'index', name, ten_colors[:cluster_number], True)
    else:
        name = "Relative number of events per 1M people in [" + str(selected_year_min) + ", " + \
                            str(selected_year_max) + "]"
        return mapping.get_new_map(df_for_map, 'relative_1M_count', name, ten_colors)


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
        choices.append(str(round(current/divider, 2)) + text + '-' + str(round(current_max/divider, 2)) + text)
        current = current + step
        if i == steps_number - 2:
            current_max = max_value
        else:
            current_max = current_max + step

    df[column + '_level'] = np.select(conditions, choices, default='unknown')

    return df


def create_country_year_extended(df_country_year):
    df_tmp = df_country_year.copy()
    for country in df_tmp['country'].unique().tolist():
        df_c = df_tmp[df_tmp['country'] == country]
        df_c = df_c.reset_index(drop=True)
        for year in df_tmp['year'].unique().tolist():
            df = df_c[df_c['year'] == year]
            if len(df) == 0:
                vals = df_c.loc[0].values.tolist()
                # vals = vals[-len(vals)+1:]
                vals[1] = year
                vals[-2] = 0
                vals[-1] = 0
                df_tmp.loc[-1] = vals  # adding a row
                df_tmp.index = df_tmp.index + 1  # shifting index
    df_tmp = df_tmp.sort_values(['country', 'year'])
    df_tmp = df_tmp.reset_index(drop=True)
    return df_tmp


def create_country_source_year_extended(df_country_source_year):
    df_tmp = df_country_source_year.copy()
    for country in df_tmp['country'].unique().tolist():
        df_c = df_tmp[df_tmp['country'] == country]
        df_c = df_c.reset_index(drop=True)
        for year in df_tmp['year'].unique().tolist():
            df = df_c[df_c['year'] == year]
            if len(df) == 0:
                vals = df_c.loc[0].values.tolist()
                # vals = vals[-len(vals)+1:]
                vals[2] = year
                vals[-2] = 0
                vals[-1] = 0
                df_tmp.loc[-1] = vals
                df_tmp.index = df_tmp.index + 1
    df_tmp = df_tmp.sort_values(['country', 'year'])
    df_tmp = df_tmp.reset_index(drop=True)
    return df_tmp
