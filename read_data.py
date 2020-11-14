import os
import pandas as pd

folder = 'data'


def get_relative_path(name):
    dirname = os.path.abspath(os.getcwd())
    file_name = os.path.join(os.path.join(dirname, folder), name)
    return file_name


def read_df(name, separator):
    file_name = get_relative_path(name)

    if os.path.exists(file_name):
        df = pd.read_csv(file_name, sep = separator)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df
    else:
        print("File {filepath} not found...".format(filepath = file_name))


def read_data():
    df_country = read_df('elsewhere_events_dataset_processed_country.csv', ',')
    print("Data df_country was read")
    df_country_year = read_df('elsewhere_events_dataset_processed_country_year.csv', ',')
    print("Data df_country_year was read")
    df_country_source_year = read_df('elsewhere_events_dataset_processed_country_source_year.csv', ',')
    print("Data df_country_source_year was read")
    df_city_year = read_df('elsewhere_events_dataset_processed_city_year.csv', ',')
    print("Data df_city_year was read")
    df_city = read_df('elsewhere_events_dataset_processed_city.csv', ',')
    print("Data df_city was read")

    return dict(country=df_country, country_year=df_country_year,
                country_source_year=df_country_source_year,
                city_year=df_city_year, city=df_city)
