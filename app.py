import streamlit as st 
import pandas as pd 
import plotly_express as px

# Read file
df = pd.read_csv('vehicles_us.csv')

# Create a text header above the dataframe
st.header('Car Sales Advertisements') 

# Display the dataframe with streamlit
st.dataframe(df)

# Create header scatteplot
st.header('Average Odometer and Price of Car Vehicles By Manufacturer and Model') 

# Find brand and type by splitting 'model' string
df[['brand', 'type']] = df['model'].str.split(' ', n=1, expand= True)

# Find the average odometer of car models plotted against average price (o_p)
# Select model, brand, price and odometer
o_p = df[['model','brand','price','odometer']]

# Group by model and brand to find the average mean price
o_p_g = o_p.groupby(['model','brand']).mean().reset_index()

# Round price and odometer values to nearest tenth value
o_p_g['price'] = round(o_p_g['price'],-1)
o_p_g['odometer'] = round(o_p_g['odometer'],-1)

# Create histogram with plot.ly, set odometer and price to x and y respectively, set color to brand
fig = px.scatter( o_p_g, x='odometer', y= 'price', hover_data= 'model', color= 'brand')

# Name axis titles and title
fig.update_layout(xaxis_title='Odometer (miles)', yaxis_title=('Price (USD)'), 
                  title= 'Average Odometer and Price of Car Vehicles By Brand',
                 legend_title = 'Brand')

# Display the figure with streamlit 
st.write(fig)

st.header("Histogram of 'condition' vs 'model _year'") 
fig = px.histogram( df, x= 'model_year', color='condition') 

st.write(fig)

st.header('Compare price distribution between manufacturers')
# get a list of car manufacturers
manufac_list = sorted(df['brand'].unique())
# get user's inputs from a dropdown menu
manufacturer_1 = st.selectbox(
                              label='Select manufacturer 1', # title of the select box
                              options=manufac_list, # options listed in the select box
                              index=manufac_list.index('chevrolet') # default pre-selected option
                              )
# repeat for the second dropdown menu
manufacturer_2 = st.selectbox(
                              label='Select manufacturer 2',
                              options=manufac_list, 
                              index=manufac_list.index('hyundai')
                              )
# filter the dataframe 
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]

# add a checkbox if a user wants to normalize the histogram
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

# create a plotly histogram figure
fig = px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay')
# display the figure with streamlit
fig = px.histogram(df_filtered, x='price', nbins=30, color='manufacturer', historm=histnorm, barmode='overlay')

# display the figure with streamlit 
st.write(fig)
                                         