# Accepts: nothing
# Returns: nothing

def clean_spott_api():
    spott_df = pd.read_csv('spott_df.csv')
    
    # Drop excess columns
    spott_df = spott_df.drop(columns='Unnamed: 0')


def clean_waqi_api():
    waqi_df = pd.read_csv('waqi_df.csv')
    
    # Drop excess columns
    waqi_df = waqi_df.drop(columns=['Unnamed: 0', 'uvi', 'date'])
    
    # Change column names
    waqi_df = waqi_df.rename(columns={'cities': 'Cities', 'aqi': 'AQI','latitude': 'Latitude', 'longitude': 'Longitude', 'pm25': 'PM25', 'pm10': 'PM10', 'o3':'O3'})
    
    

def clean_and_combine_df():
    # Merge
    combined_df = spott_df.merge(waqi_df, how='inner', on='Cities')
    
    # Drop columns with NA values
    combined_df = combined_df.dropna()
    
    # Reset index
    combined_df = combined_df.reset_index().drop(columns='index')




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

def create_map():
    # Create base for Map
    my_map = folium.Map(
        min_zoom=1.5,
        max_zoom=18, 
        zoom_start=10
    )
    
    # Add markers for each city
    for i in range(len(cities.Cities)):
        city = cities.loc[i]
        folium.Marker(
            location=[city['Latitude'], city['Longitude']],
            popup=city['Summary'],
            tooltip=city['Cities'],
            icon=folium.Icon(color=city['Marker_Color'], prefix='fa', icon='circle'),
        ).add_to(my_map)  
    
    my_map

