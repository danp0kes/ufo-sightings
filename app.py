# Import appropriate packages
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import calendar

# Read file
df = pd.read_csv('ufo-sightings-transformed.csv', parse_dates=['Date_time'])

# Drop unnamed column
df = df.iloc[:,1:]

# Make columns lowercase for easier referencing
df.columns = df.columns.str.lower()

# Change name of confusing duration column name
df = df.rename(columns= {'length_of_encounter_seconds':'duration_secs'})

# Change month number to month name
df['month'] = df['month'].apply(lambda x: calendar.month_name[x])

# Create duration in minutes column
df['duration_mins'] = df['duration_secs'] / 60

# Create duration in hours
df['duration_hours'] = df['duration_mins'] / 60

# Create duration in days 
df['duration_days'] = df['duration_hours'] / 24

# Create age column as 2023 minus the year and month

df['age'] = 2023 - (df['date_time'].dt.year + (df['date_time'].dt.month/12))

# Create a text header above the dataframe
st.header('UFO Sightings') 

# Create header scatterplot
st.write("""
##### Introduction
The data contains information about UFO encounters from 1906 to 2014. Details about the shape of the UFO, the duration of the encounter and as well as the co-ordinates of its location have all been recorded. Our analysis will look at these elements on a histogram, scatterplot and a map.
""") 

# Save list of countries as countries
countries = df['country'].unique()

# Create select box to filter by country
name_country = st.selectbox('Select country:',countries)

# Save min and max years for slider
duration_min, duration_max = (df['duration_hours'].min(), df['duration_hours'].max())

# Create header scatterplot
st.write("""
##### Filter encounters by the duration length
""") 

# Create slider using min and max years
duration_range = st.slider('Choose duration lengths (hours):', value=(duration_min, duration_max) , min_value=duration_min, max_value=duration_max)


#save filtered df as the 
filtered_df = df[(df['country'] == name_country) & (df['duration_hours'] > duration_range[0])]# & df[df['duration_hours'] < duration_range[1]]]
              
# Display the dataframe with streamlit
st.table(filtered_df.head(5))

# Create histogram header
st.header('Duration Analysis')

st.write("""
###### Does the duration of the encounter change depending on the shape of the observed ufo? The state it is observed in? How about the month or season?
""")

# Create dataframes for different duration lengths by dynamically setting variables
d = {}
d['minute'] = filtered_df[filtered_df['duration_mins'] <= 1]
d['hour'] = filtered_df[filtered_df['duration_hours'] <= 1]
d['day'] = filtered_df[filtered_df['duration_days'] <= 1]
d['millenia'] = filtered_df

# Create selection box for duration length
duration_for_hist = st.selectbox('duration length by first:',  ['minute','hour','day','millenia'])

# Create list for histogram variables
var_list_for_hist= ['region', 'ufo_shape', 'season', 'month']

# Create selection box for region, shape, season and month
var_for_hist = st.selectbox('split for duration distribution:', var_list_for_hist)

# Provide changes to x-axis dependent on the above selectbox
e = {}
e['minute'] = 'duration_secs'
e['hour'] = 'duration_mins'
e['day'] = 'duration_hours'
e['millenia'] = 'duration_days'

# Order months for legend
months_ordered = ['January', 'February', 'March', 'April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Create histogram
fig = px.histogram(d[duration_for_hist], x=e[duration_for_hist], color=var_for_hist, category_orders={'month': months_ordered})

# Rename axis, title and legend
fig.update_layout(title= 'Split of encounter duration by {}</b>'.format(var_for_hist))

# Display the Chart
st.plotly_chart(fig)

# Create scatterplot header
st.header('Age Analysis')

st.write("""
###### How does the age of a reported case affect duration in terms of country, season and month
""")

# Create dataframes for different duration lengths by dynamically setting variables
f = {}
f['minute'] = df[df['duration_mins'] <= 1]
f['hour'] = df[df['duration_hours'] <= 1]
f['day'] = df[df['duration_days'] <= 1]
f['millenia'] = df

# Create selection box for duration length
duration_for_scatter = st.selectbox('duration length by first:',  ['minute','hour','day','millenia'], key=1)

list_for_scatter= ['country', 'season', 'month'] 
choice_for_scatter= st.selectbox('filter by:', list_for_scatter)

fig2= px.scatter(f[duration_for_scatter], x=e[duration_for_scatter], y='age' , color=choice_for_scatter, hover_data='description',category_orders={'month': months_ordered})

st.plotly_chart(fig2)

# Create scatterplot header
st.header('A Map of UFO Encounters')

st.write("""
###### Here are the encounters presented on a map. UFO shapes can be selected to show where different shapes have been found around the world. Sorting by duration and age will change the size of each bubble.
""")

# Find unique shapes
shapes= df['ufo_shape'].unique()


# Create 
shapes_for_map = st.selectbox('Shape of the sighted UFO:', shapes)

# Create variables to measure by for map
list_for_map= ['duration_secs','age'] 
choice_for_map= st.selectbox('increase bubble size by:', list_for_map)

st.map(df[df['ufo_shape'] == shapes_for_map], latitude='latitude', longitude='longitude', size=list_for_map, color = [1.0, 0.5, 0, 0.2])

st.write("""
###### Interestingly, the only hexagon shaped UFO has said to have been spotted in Pittsburgh. Two crescents have been spotted in Wisconsin and New Hampshire.
""")