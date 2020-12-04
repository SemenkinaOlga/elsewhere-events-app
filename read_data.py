import os
import pandas as pd

folder = 'data'


def get_relative_path(name, current_folder=""):
    dirname = os.path.abspath(os.getcwd())
    file_name = os.path.join(dirname, folder)
    if current_folder != "":
        file_name = os.path.join(file_name, current_folder)
    file_name = os.path.join(file_name, name)
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


def write_df(df, name):
    out_file_name = os.path.join(os.getcwd(), name)
    df.to_csv(out_file_name, index=False)


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
    df_country_year_extended = read_df('elsewhere_events_dataset_processed_country_year_extended.csv', ',')
    print("Data df_country_year_extended was read")
    df_country_source_year_extended = read_df('elsewhere_events_dataset_processed_country_source_year_extended.csv', ',')
    print("Data df_country_source_year_extended was read")

    return dict(country=df_country, country_year=df_country_year,
                country_source_year=df_country_source_year,
                city_year=df_city_year, city=df_city,
                country_year_extended=df_country_year_extended,
                country_source_year_extended=df_country_source_year_extended)
