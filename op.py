import streamlit as st
import pandas as pd
import mysql.connector

# Function to fetch data from MySQL database
def fetch_data():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Krishna3_6_9',
            database='route'
        )
        query = "SELECT * FROM bus_routes"
        df = pd.read_sql(query, conn)
        return df
    except mysql.connector.Error as err:
        st.error(f"Database connection error: {err}")
    finally:
        if conn:
            conn.close()

# Load data
df = fetch_data()

# Streamlit app layout
st.title("Bus Routes Explorer")
st.markdown("### Find the best bus routes based on your preferences")

# Sidebar for filtering
st.sidebar.header("Filter Options")

# Filter by State
states = df['Route_name'].unique()
selected_state = st.sidebar.selectbox("Select State", states)

# Filter by Comfort Level
comfort_levels = df['Bus_type'].unique()
selected_comfort = st.sidebar.selectbox("Select Comfort Level", comfort_levels)

# Filter by Max Price
max_price = st.sidebar.number_input("Max Price (INR)", min_value=0, 
                                     value=int(df['Price'].max()), step=100)

# Filter by Min Rating
min_rating = st.sidebar.slider("Min Rating", min_value=0.0, max_value=5.0, 
                                value=0.0, step=0.1)

# Filter data
filtered_df = df[(df['Route_name'] == selected_state) &
                 (df['Bus_type'] == selected_comfort) &
                 (df['Price'] <= max_price) & 
                 (df['Ratings'] >= min_rating)]

# Display filtered data
if not filtered_df.empty:
    st.write("### Filtered Bus Routes")
    st.dataframe(filtered_df)

    # Show additional stats
    st.write(f"Total Routes Found: {len(filtered_df)}")

    # Price distribution for the bar chart
    price_bins = range(0, int(df['Price'].max()) + 100, 100)
    price_counts = pd.cut(filtered_df['Price'], bins=price_bins).value_counts().sort_index()
    
    st.bar_chart(price_counts)

else:
    st.write("No routes found with the selected criteria. Please adjust your filters.")

# Footer
st.markdown("---")
st.write("Explore more bus routes with different filters and enjoy your journey!")
s