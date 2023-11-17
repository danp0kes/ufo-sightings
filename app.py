# Import appropriate packages
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import calendar
import plotly.graph_objects as go

# Read and clean data
# Read file
df = pd.read_csv('ufo-sightings-transformed.csv', parse_dates=['Date_time'])

# Drop unnamed column
df = df.iloc[:, 1:]

# Make columns lowercase for easier referencing
df.columns = df.columns.str.lower()

# Change name of confusing duration column name
df = df.rename(columns={'length_of_encounter_seconds': 'duration_secs'})

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

# Replace '&#44' with ' in description column
df['description'] = df['description'].str.replace('&#44', "")

# Replace '&#39' with ' in description column
df['description'] = df['description'].str.replace('&#39', "")

# Replace '&#33' with '.' in description column
df['description'] = df['description'].str.replace('&#33', '.')

# Create a text header above the dataframe
st.header('UFO Sightings')

# Create header scatterplot
st.write("""
##### Introduction
The data contains information about UFO encounters from 1906 to 2014. Details about the shape of the UFO, the duration of the encounter as well as the co-ordinates of its location have all been recorded. Our analysis will look at these elements on a histogram, scatterplot and an interactive map.
""")

# Display the dataframe with streamlit
st.table(df.drop(columns='description').head(10))

# Create histogram header
st.header('Duration Analysis')

st.write("""
###### Does the duration of the encounter change depending on the shape of the observed ufo? The country and state it is observed in? How about the month or season?
""")

# Create selection box for duration length
duration_for_hist = st.selectbox('Duration length by first:',  [
                                 'minute', 'hour', 'day'])

# Save list of countries as countries
countries = df['country'].unique()

# Create select box to filter by country
name_country = st.selectbox('Select country:', countries)

# Dynamically create variables to provide changes to x-axis dependent on the duration selectbox
d = {}
d['minute'] = 'duration_secs'
d['hour'] = 'duration_mins'
d['day'] = 'duration_hours'
d['millenia'] = 'duration_days'

# Dynamically create variables to provide changes to x-axis dependent on the duration selectbox
e = {}
e['minute'] = 'duration_mins'
e['hour'] = 'duration_hours'
e['day'] = 'duration_days'

# Create filtered df by combining country and duration length
filtered_df = df[(df['country'] == name_country) &
                 (df[e[duration_for_hist]] < 1)]

# Create list for histogram variables
var_list_for_hist = ['region', 'ufo_shape', 'season', 'month']

# Create selection box for region, shape, season and month
var_for_hist = st.selectbox(
    'Split for duration distribution:', var_list_for_hist)

# Order months for legend
months_ordered = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                  'September', 'October', 'November', 'December']

# Create histogram
fig = px.histogram(filtered_df, x=d[duration_for_hist], color=var_for_hist, category_orders={
                   'month': months_ordered}, nbins=24)

# Rename axis, title and legend
fig.update_layout(
    title='Split of encounter duration by {}</b>'.format(var_for_hist))

# Display the Chart
st.plotly_chart(fig)

# Create scatterplot header
st.header('Age Analysis')

st.write("""
###### How does the age of a reported case affect duration in terms of country, season and month?
""")

# Create dataframes for different duration lengths by dynamically setting variables
f = {}
f['minute'] = df[df['duration_mins'] <= 1]
f['hour'] = df[df['duration_hours'] <= 1]
f['day'] = df[df['duration_days'] <= 1]
f['millenia'] = df

# Create selection box for duration length
duration_for_scatter = st.selectbox('Duration length by first:',  [
                                    'minute', 'hour', 'day', 'millenia'], key=1)

list_for_scatter = ['country', 'season', 'month']
choice_for_scatter = st.selectbox('Filter by:', list_for_scatter)

fig2 = px.scatter(f[duration_for_scatter], x=d[duration_for_scatter], y='age', color=choice_for_scatter,
                  hover_data='description', category_orders={'month': months_ordered})

st.plotly_chart(fig2)

# Create scatterplot header
st.header('A Map of UFO Encounters')

st.write("""
###### Here are the encounters presented on a map. UFO shapes can be selected to show where different shapes have been found around the world. Each encounter is colored based on the age it was last seen. When hovering, a description by the viewer is given.
""")

# Find unique shapes
shapes = df['ufo_shape'].unique()

# Create shapes select box
shapes_for_map = st.selectbox('Shape of the sighted UFO:', shapes)

# Create color scale
scl = [0, "rgb(150,0,90)"], [0.125, "rgb(0, 0, 200)"], [0.25, "rgb(0, 25, 255)"], \
    [0.375, "rgb(0, 152, 255)"], [0.5, "rgb(44, 255, 150)"], [0.625, "rgb(151, 255, 0)"], \
    [0.75, "rgb(255, 234, 0)"], [0.875, "rgb(255, 111, 0)"], [
    1, "rgb(255, 0, 0)"]

# create new df according to ufo_shape
df1 = df[df['ufo_shape'] == shapes_for_map]

# Create geographical scatterplot, add colorbar to show age
fig3 = go.Figure(data=go.Scattergeo(
    lat=df1['latitude'],
    lon=df1['longitude'],
    text=df1['description'],
    marker=dict(
        color=df1['age'],
        colorscale=scl,
        reversescale=True,
        opacity=0.7,
        size=5,
        colorbar=dict(
            titleside='top',
            outlinecolor='rgba(68, 68, 68, 0)',
            title='Age'
        )
    )
))

# Change layout to make it easier to view, add a title
fig3.update_layout(
    geo=dict(
        scope='world',
        showland=True,
        landcolor='rgb(212, 212, 212)',
        subunitcolor='rgb(255, 255, 255)',
        countrycolor='rgb(255, 255, 255)',
        showlakes=True,
        lakecolor='rgb(255, 255, 255)',
        showsubunits=True,
        showcountries=True,
        resolution=110,
    ),
    title='Encounters Where the UFO Shape is a {}'.format(shapes_for_map),
    height=800,
    width=1000


)
st.plotly_chart(fig3)

st.write("""
###### Interestingly, the only dome and hexagon shaped UFO have said to have been spotted in Pittsburgh. Two crescents have been spotted in Wisconsin and New Hampshire.
""")
