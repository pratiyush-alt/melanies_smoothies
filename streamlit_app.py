# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Set Streamlit app title and instructions
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your Smoothie!")

# User input for name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get the current Snowflake session
session = get_active_session()

# Get list of available fruits from the Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Let the user select fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,max_selections= 5
)

# Proceed if fruits are selected
if ingredients_list:
    # Create a string of ingredients
    ingredients_string = ', '.join(ingredients_list)

    # Construct correct INSERT statement with both columns specified
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}')
    """

    # Button to submit order
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('✅ Your Smoothie is ordered!')
