import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd  # 🎯 Bringing in Pandas

st.title(":strawberry: Customize Your Smoothie! :strawberry:")
st.write("Choose the fruits you want in your custom Smoothie!")

cnx = st.connection("snowflake")
session = cnx.session()

# 🥋 Updated to include the SEARCH_ON column
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# 🥋 Convert the Snowpark Dataframe to a Pandas Dataframe so we can use LOC
pd_df = my_dataframe.to_pandas()

name_on_order = st.text_input('Name on Smoothie:')

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe, # Still uses the Snowflake df for the list
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        # 🥋 The "Strange-Looking Statement"
        # This looks for the FRUIT_NAME in our pandas df and grabs the matching SEARCH_ON value
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        # Update the API call to use the search_on variable
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
