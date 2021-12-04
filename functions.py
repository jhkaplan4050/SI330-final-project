import pandas as pd
import folium

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats




# Accepts: nothing
# Returns: nothing

def clean_spott_api(name):
    spott_df = pd.read_csv(name)
    
    # Drop excess columns
    spott_df = spott_df.drop(columns='Unnamed: 0')
    
    return spott_df


def clean_waqi_api(name):
    waqi_df = pd.read_csv(name)
    
    # Drop excess columns
    waqi_df = waqi_df.drop(columns=['Unnamed: 0', 'uvi', 'date'])
    
    # Change column names
    waqi_df = waqi_df.rename(columns={'cities': 'Cities', 'aqi': 'AQI','latitude': 'Latitude', 'longitude': 'Longitude', 'pm25': 'PM25', 'pm10': 'PM10', 'o3':'O3'})
    
    return waqi_df
    
    
#df1 = spott
#df2 = waqi
def clean_and_combine_df(df1, df2):
    # Merge
    combined_df = df1.merge(df2, how='inner', on='Cities')
    
    # Drop columns with NA values
    combined_df = combined_df.dropna()
    
    # Reset index
    combined_df = combined_df.reset_index().drop(columns='index')


    return combined_df

# Accepts: string
# Returns: int

def aqi_to_int(aqi):
    return int(aqi)




# Accepts: int
# Returns: string

def create_marker_color(aqi):
    if (aqi>=0) and (aqi<=50):
        return "green"
    elif (aqi>=51) and (aqi<=100):
        return "yellow"
    elif (aqi>=101) and (aqi<=150):
        return "orange"
    elif (aqi>=151) and (aqi<=200):
        return "red"
    elif (aqi>=201) and (aqi<=300):
        return "purple"
    elif aqi>= 301:
        return "maroon"
    else:
        return "white"




# Accepts: dataframe
# Returns: string

def create_summary(df):
    name = df['Cities']
    population = df['Population']
    elevation = df['Elevation']
    aqi = df['AQI']
    return f"Name: {name} \n Population: {population} \n Elevation: {elevation} \n AQI: {aqi} \n"



# Accepts: nothing
# Returns: dataframe

def prep_cities_for_mapping():
    # Read in cities dataframe
    cities = pd.read_csv('combined_df.csv')
    
    # Drop excess columns
    cities = cities.drop(columns='Unnamed: 0')
    
    # Drop rows with "-" as the AQI value
    index_names = cities[cities['AQI'] == '-'].index
    cities.drop(index_names, inplace = True)
    
    # Change AQI to integers
    cities['AQI'] = cities['AQI'].apply(aqi_to_int)
    
    # Make market colors
    cities['Marker_Color'] = cities['AQI'].apply(create_marker_color)
    
    # Create summary 
    cities['Summary'] = cities.apply(create_summary, axis=1)
    
    return cities



# Accepts: nothing
# Returns: nothing

def create_map(df):
    # Create base for Map
    my_map = folium.Map(
        min_zoom=1.5,
        max_zoom=18, 
        zoom_start=10
    )
    
    # Add markers for each city
    for i in range(len(df.Cities)):
        city = df.loc[i]
        folium.Marker(
            location=[city['Latitude'], city['Longitude']],
            popup=city['Summary'],
            tooltip=city['Cities'],
            icon=folium.Icon(color=city['Marker_Color'], prefix='fa', icon='circle'),
        ).add_to(my_map)  
    
    my_map


def to_int(aqi):
    if aqi != '-':
        return int(aqi)
    else:
        return None


def clean_df(csv_file):
    combined_df = pd.read_csv(csv_file)
    combined_df['AQI'] = combined_df['AQI'].apply(to_int)
    combined_df = combined_df.dropna()
    return combined_df


def set_parameters(combined_df):
    params_dict = {}
    params_dict['aqi'] = combined_df['AQI']
    params_dict['population'] = combined_df['Population']
    params_dict['elevation'] = combined_df['Elevation']
    params_dict['pm25'] = combined_df['PM25']
    params_dict['pm10'] = combined_df['PM10']
    params_dict['o3'] = combined_df['O3']
    return params_dict


def create_figure1(params):
    x = params['aqi']
    y1 = params['population']
    m, b = np.polyfit(x, y1, 1)

    #create Figure 1: AQI vs Population
    plt.plot(x, y1, 'o', color = "#BF4D27")
    plt.plot(x, m*x + b)
    plt.rcParams["figure.autolayout"] = False
    plt.xlabel("Air Quality Index")
    plt.ylabel("Population (in tens of millions)")
    plt.title("Figure 1")
    font = {'size'   : 18, 'family': "Times New Roman","sans-serif":"Arial"}
    plt.rc('font', **font)
    plt.show()
    #correlation coefficient, p-value
    print("correlation coefficient, p-value:", stats.pearsonr(aqi, population))
    

def create_figure2():
    params = set_parameters()
    x = params['aqi']
    y2 = params['elevation']
    m, b = np.polyfit(x, y2, 1)

    #create Figure 2: AQI vs Elevation
    plt.plot(x, y2, 'o', color = "#4F7B28")
    plt.plot(x, m*x + b)
    plt.xlabel("Air Quality Index")
    plt.ylabel("Elevation (ft)")
    plt.title("Figure 2")
    font = {'size'   : 18, 'family': "Times New Roman","sans-serif":"Arial"}
    plt.rc('font', **font)
    plt.show()
    
    #correlation coefficient, p-value
    print("correlation coefficient, p-value:", stats.pearsonr(aqi, elevation))


def create_figure3():
    params = set_parameters()
    x = params['aqi']
    y3 = params['pm25']
    m, b = np.polyfit(x, y3, 1)

    plt.plot(x, y3, 'o', color = "#abdbe3")
    plt.plot(x, m*x + b)

    #create Figure 3: AQI vs PM25
    plt.xlabel("Air Quality Index")
    plt.ylabel("PM25 (µg/m³)")
    plt.title("Figure 3")
    font = {'size'   : 18, 'family': "Times New Roman","sans-serif":"Arial"}
    plt.rc('font', **font)
    plt.show()
    
    #correlation coefficient, p-value
    print("correlation coefficient, p-value:", stats.pearsonr(aqi, pm25))


def create_figure4():
    params = set_parameters()
    x = params['aqi']
    y4 = params['pm10']
    m, b = np.polyfit(x, y4, 1)

    plt.plot(x, y4, 'o', color = "#28767B")
    plt.plot(x, m*x + b)

    #create Figure 4: AQI vs PM10
    #plt.scatter(aqi, pm10, color = "#28397B")
    plt.xlabel("Air Quality Index")
    plt.ylabel("PM10 Levels (µg/m³)")
    plt.title("Figure 4")
    font = {'size'   : 18, 'family': "Times New Roman","sans-serif":"Arial"}
    plt.rc('font', **font)
    plt.show()
    
    #correlation coefficient, p-value
    print("correlation coefficient, p-value:",stats.pearsonr(aqi, pm10))

def create_figure5():
    params = set_parameters()
    x = params['aqi']
    y5 = params['o3']
    m, b = np.polyfit(x, y5, 1)

    plt.plot(x, y5, 'o', color = "#63287B")
    plt.plot(x, m*x + b)

    #create Figure 5: AQI vs O3
    plt.xlabel("Air Quality Index")
    plt.ylabel("O3 Levels")
    plt.title("Figure 5")
    font = {'size'   : 18, 'family': "Times New Roman","sans-serif":"Arial"}
    plt.rc('font', **font)
    plt.show()
    
    #correlation coefficient, p-value
    print("correlation coefficient, p-value:",stats.pearsonr(aqi, o3))

