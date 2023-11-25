# Import appropriate packages
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

# Read and clean data
# Read file
df = pd.read_csv('ufo-sightings-cleaned.csv', parse_dates=
                 ['encounter_date','reported_diff'], infer_datetime_format=True)

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
st.header('Frequency Analysis')

st.write("""
###### How frequently are sightings occurring? How does this change over time? 
""")

# Find min and max encounter years
(min_year,max_year) = (df['encounter_date'].dt.year.min(),df['encounter_date'].dt.year.max())

# Create slider for encounter years
year_range = st.slider('Select a range of years:', min_year, max_year, (min_year, max_year))

# Create selection box for duration length
legend_variable = st.selectbox('Filter by:',[
                                 'Season', 'Continent','Time of Day'], 
                               key=1)

# Create new dataframe with filtered years
filtered_df = df[(df['encounter_date'].dt.year >= year_range[0]) & (
    df['encounter_date'].dt.year <= year_range[1])]

# Save legend_variable to reference appropriate legend columns in histogram
d={}
d['Season'] = 'season'
d['Continent'] = 'continent'
d['Time of Day'] = 'time_of_day'


# Save legend_variable to reference appropriate category orders in histogram
e={}
e['Season'] = ['Spring', 'Summer', 'Autumn', 'Winter']
e['Continent'] = ['North America', 'South America', 'Europe', 'Asia', 'Africa', 'Oceania']
e['Time of Day'] = ['Morning', 'Afternoon', 'Evening', 'Night']

# Create histogram of ufo sightings duration per continent
fig = px.histogram(filtered_df, 
                   x='encounter_year', 
                   color=d[legend_variable], 
                   title='UFO Sightings Duration per Continent', 
                   labels={'duration_secs':'Duration (minutes)', 'continent':'Continent'},
                   category_orders={d[legend_variable]:e[legend_variable]})

# Update layout
fig.update_layout(
    title={
        'text': f"UFO Sightings Count and Duration per {legend_variable}",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Duration (minutes)",
    yaxis_title="Number of Sightings",
    legend_title="Continent",
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="RebeccaPurple"
    )
)

st.plotly_chart(fig)

st.write("Encounters are increasing at a dramatic rate. More encounters are now occurring in Summer when Autumn used to have more."
)
#----------------------------------------------------------------------------------------------------------------------------

st.header('Report Date Lag')

# write string in streamlit
st.write("""Validity may be tested by comparing the relationship of the duration 
         of an encounter with the encounter-report age lag (the difference between 
         the encounter date and the date it was reported). In short, this answers 
         whether the details of the story might change over time. Where there is a 
         large encounter-report date gap, perhaps the duration is being reported 
         longer than those with a smaller gap.
         """)

# Create slider for encounter years
year_range2 = st.slider('Select a range of years:', min_year, max_year, (min_year, max_year), key=2)

# Create selection box for report date lag
legend_variable2 = st.selectbox('Filter by:',['Season', 'Continent','Time of Day'], key=3)

# Create new dataframe with filtered years
filtered_df2 = df[(df['encounter_date'].dt.year >= year_range[0]) & (
    df['encounter_date'].dt.year <= year_range[1])]

# Filter dataframe to only include encounters with less than 1 hour duration (filter out outliers)
filtered_df2 = filtered_df2[filtered_df2['duration_hours'] <= 1]

# Create scatter plot with specific colors for each month
fig2 = px.scatter(filtered_df2, 
                 x='reported_diff', 
                 y='duration_mins', 
                 color=d[legend_variable], 
                 category_orders={d[legend_variable]:e[legend_variable]},
                 opacity=0.5
                 )

# Update titles
fig2.update_layout(
    title={
        'text': "Report Date Lag and Encounter Duration",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Reported Difference (years)",
    yaxis_title="Duration (mins)",
    legend_title='Season',
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="black")
    
)

st.plotly_chart(fig2)

st.write("""
If we expected a reported duration to increase over time the scatter plot would reflect this. 
This doesn't seem to be 
the case as every encounter with a report lag of sixty years plus 
do not exceed those found in previous years.
""")
#----------------------------------------------------------------------------------------------------------------------------

# Create mape header
st.header('A Map of UFO Encounters')

st.write("""
###### Here are the encounters presented on a map. UFO shapes can be selected to show where different shapes have been found around the world. Each encounter is colored based on the age it was last seen. When hovering, a description by the viewer is given.
""")

# Create radio
radio = st.radio('Select a map:', ['World View', 'United States'])

# Create new dataframe with only United States encounters
united_states_df = df[df['country'] == 'United States']

# Find unique shapes and colors
shapes = df['ufo_shape'].unique()
colors = df['ufo_color'].unique()

# Add 'All' option to shapes and colors
shapes = np.append(shapes, 'All').astype(str)
colors = np.append(colors, 'All').astype(str)

# Re-order shapes and colors using sorted
shapes = sorted(shapes)
colors = sorted(colors)

#If united states is checked, filter df to only include united states
if radio == 'United States':
    united_states_df = df[df['country'] == 'United States'] 

# Create shapes select box
shapes_for_map = st.selectbox('Shape of the sighted UFO:', shapes)

# Create color select box
colors_for_map = st.selectbox('Color of the sighted UFO:', colors)

# Allow user to select all shapes
if shapes_for_map == 'All' and colors_for_map == 'All':
    filtered_df3 = df
    
# Allow user to select all colors
elif colors_for_map == 'All':
    filtered_df3 = df[(df['ufo_shape'] == shapes_for_map)]
    
# Allow user to select all shapes
elif shapes_for_map == 'All':
    filtered_df3 = df[(df['ufo_color'] == colors_for_map)]

# Create geographical scatterplot, add colorbar to show age, zoom in on united states
if radio == 'United States':
    scope='usa'
else:
    scope='world'
    
# Create color scale
scl = [0, "rgb(150,0,90)"], [0.125, "rgb(0, 0, 200)"], [0.25, "rgb(0, 25, 255)"], \
    [0.375, "rgb(0, 152, 255)"], [0.5, "rgb(44, 255, 150)"], [0.625, "rgb(151, 255, 0)"], \
    [0.75, "rgb(255, 234, 0)"], [0.875, "rgb(255, 111, 0)"], [
    1, "rgb(255, 0, 0)"]
    
# Create geographical scatterplot
fig3 = go.Figure(data=go.Scattergeo(
    lat=filtered_df3['latitude'],
    lon=filtered_df3['longitude'],
    text=filtered_df3['description'],
    marker=dict(
        color=filtered_df3['age'],
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

fig3.update_layout(
    geo=dict(
        scope=scope,
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
    title=f'Encounters Where the UFO Shape is {shapes_for_map} and Color is {colors_for_map}',
)

st.plotly_chart(fig3)

st.write("""
###### Interestingly, the only dome and hexagon shaped UFO have said to have been spotted in Pittsburgh. Two crescents have been spotted in Wisconsin and New Hampshire.
""")
