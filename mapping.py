import os
import pandas as pd
import folium
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup
import vincent
import json
import branca

import read_data as rd

map_folder = 'country coordinates'
zoom_start = 1
location = [27.664827, -81.516]
location_zero = [27, 0]


def get_simple_map(df, value_col, title, colors, steps=False):
    current_map = folium.Map(location=location_zero, zoom_start=zoom_start)

    ma = max(df[value_col])
    mi = min(df[value_col])

    if steps:
        colormap = branca.colormap.StepColormap(
            vmin=int(mi),
            vmax=int(ma),
            colors=colors,
            # index=[mi,(ma-mi)*0.3+mi,(ma-mi)*0.6+mi,(ma-mi)*0.8+mi,ma],
            caption=title,
        )
    else:
        colormap = branca.colormap.LinearColormap(
            vmin=int(mi),
            vmax=int(ma),
            colors=colors,
            # index=[mi,(ma-mi)*0.3+mi,(ma-mi)*0.6+mi,(ma-mi)*0.8+mi,ma],
            caption=title,
        )

    colormap.add_to(current_map)
    name_country = df['code']

    value = df[value_col].tolist()

    def stile(k):
        return lambda x: {
            'fillColor': colormap(value[k]),
            "color": "black",
            "fillOpacity": 0.7,
        }

    tooltip = []
    for i in range(len(df)):
        tooltip.append(GeoJsonTooltip(
            fields=["name"],
            aliases=["Country:"],
            localize=True,
            sticky=False,
            labels=True,
            style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
            max_width=800,
        ))

    for i in range(len(df)):
        file_name = rd.get_relative_path(str(name_country[i]) + ".geo.json", map_folder)
        if os.path.exists(file_name):
            current_map.add_child(folium.GeoJson(data=open(file_name, 'r', encoding='utf-8-sig').read(),
                                                 tooltip=tooltip[i], style_function=stile(i)))

    return current_map


def get_ico_map(df, value_col, title, colors, steps=False):
    current_map = folium.Map(location=location_zero, zoom_start=zoom_start)

    ma = max(df[value_col])
    mi = min(df[value_col])
    if steps:
        colormap = branca.colormap.StepColormap(
            vmin=int(mi),
            vmax=int(ma),
            colors=colors,
            # index=[mi,(ma-mi)*0.3+mi,(ma-mi)*0.6+mi,(ma-mi)*0.8+mi,ma],
            caption=title,
        )
    else:
        colormap = branca.colormap.LinearColormap(
            vmin=int(mi),
            vmax=int(ma),
            colors=colors,
            # index=[mi,(ma-mi)*0.3+mi,(ma-mi)*0.6+mi,(ma-mi)*0.8+mi,ma],
            caption=title,
        )

    colormap.add_to(current_map)
    name_country = df['code']

    value = df[value_col].tolist()

    def stile(k):
        return lambda x: {
            'fillColor': colormap(value[k]),
            "color": "black",
            "fillOpacity": 0.5,
        }

    tooltip = []
    for i in range(len(df)):
        tooltip.append(GeoJsonTooltip(
            fields=["name"],
            aliases=["Country:"],
            localize=True,
            sticky=False,
            labels=True,
            style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
            max_width=800,
        ))

    for i in range(len(df)):
        file_name = rd.get_relative_path(str(name_country[i]) + ".geo.json", map_folder)
        if os.path.exists(file_name):
            current_map.add_child(folium.GeoJson(data=open(file_name, 'r', encoding='utf-8-sig').read(),
                                                 tooltip=tooltip[i], style_function=stile(i)))

    df = pd.read_csv(rd.get_relative_path("attributes.txt", map_folder), sep=',')
    df1 = pd.read_csv(rd.get_relative_path("countries.txt", map_folder), sep=',')

    text = []
    for i in range(len(df.columns)):
        text.append(df.columns[i])

    tooltip1 = []

    for i in range(len(df1)):
        tooltip1.append(GeoJsonTooltip(
            fields=[*text],
            aliases=[*text],
            localize=True,
            sticky=False,
            labels=True,
            style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
            max_width=800,
        ))

    for i in range(len(df1)):
        file_name = rd.get_relative_path(str(df1['Country'][i]) + ".geo.json", map_folder)
        if os.path.exists(file_name):
            current_map.add_child(
                folium.GeoJson(data=open(file_name, 'r', encoding='utf-8-sig').read(), tooltip=tooltip1[i]))

    return current_map


def get_new_map(df, value_col, title, colors, steps=False):
    current_map = folium.Map(location=location_zero, zoom_start=zoom_start)

    ma = max(df[value_col])
    mi = min(df[value_col])

    if steps:
        colormap = branca.colormap.StepColormap(
            vmin=int(mi),
            vmax=int(ma),
            colors=colors,
            # index=[mi,(ma-mi)*0.3+mi,(ma-mi)*0.6+mi,(ma-mi)*0.8+mi,ma],
            caption=title,
        )
    else:
        colormap = branca.colormap.LinearColormap(
            vmin=int(mi),
            vmax=int(ma),
            colors=colors,
            # index=[mi,(ma-mi)*0.3+mi,(ma-mi)*0.6+mi,(ma-mi)*0.8+mi,ma],
            caption=title,
        )

    colormap.add_to(current_map)
    name_country = df['code']

    value = df[value_col].tolist()

    def stile(k):
        return lambda x: {
            'fillColor': colormap(value[k]),
            "color": "black",
            "fillOpacity": 0.7,
        }

    tooltip = []
    fields = ['country', 'macro_region', 'meso_region', 'development_level', 'gdp_per_capita',
              'gdp_volume', 'country_population_2018',
              'count', 'relative_1M_count']
    names = ['Country', 'Macro Region', 'Meso Region', 'Development level', 'GDP per capita',
             'GDP volume', 'Population 2018',
             'Events total amount', 'Relative per 1M events amount']

    for i in range(len(df)):
        tooltip.append(GeoJsonTooltip(
            fields=[*fields],
            aliases=[*names],
            localize=True,
            sticky=False,
            labels=True,
            style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
            max_width=800,
        ))

    for i in range(len(df)):
        file_name = rd.get_relative_path(str(name_country[i]) + ".geo.json", map_folder)
        if os.path.exists(file_name):
            data = open(file_name, 'r', encoding='utf-8-sig').read()
            if "\"type\":\"Point\"" not in data:
                current_map.add_child(folium.GeoJson(data=data,
                                                     tooltip=tooltip[i], style_function=stile(i)))

    return current_map
