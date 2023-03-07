import streamlit as st
import pandas as pd
import requests as rq
import snowflake.connector

st.title('My Parents New Healthy Diner')
st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-boiled Free-Range Egg')
st.text('🥑🍞 Avocado toast')
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)


fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)

#New Section to display fruitvice api response
fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#st.text(fruityvice_response.json()) #just writes the data to the screen


#take the json version of the response and normalize it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#output it the screen as a table
st.dataframe(fruityvice_normalized)


my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)
