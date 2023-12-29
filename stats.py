
import streamlit as st
import pip._vendor.requests as requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    st.title('Streamlit Frontend for Flask API')
    response = requests.get('http://141.147.64.158/getstatschart/')
    content = response.text  # Get the content of the response as a string
    content = content.strip()  # Now you can use the strip() method
    # st.write(f"Response status code: {response.status_code}")
    # st.write(f"Response content: {content}")

    try:
        data = response.json()
        # Convert 'data' list of dictionaries to DataFrame
        chart_data = pd.DataFrame(data)
        # Reorder columns so 'product_price' is first and 'price_date' is second
        chart_data = chart_data[['product_price_stats', 'price_date_stats']]
        chart_data['product_price_stats'] = chart_data['product_price_stats'].astype(float)
        chart_data['price_date_stats'] = pd.to_datetime(chart_data['price_date_stats']).dt.date  # Convert 'price_date' to date without time
        chart_data.sort_values('price_date_stats', inplace=True)  # Sort by 'price_date' in ascending order
        # st.write(chart_data)  # Display the DataFrame
    except Exception as e:
        st.write(f"Error: {str(e)}")
        return  # If there's an error, we return and don't attempt to draw the chart


# Create a line chart with 'product_price' on the y-axis
    try:
        fig, ax = plt.subplots()
        ax.plot(chart_data['price_date_stats'], chart_data['product_price_stats'], marker='o')  # Removed linestyle=''
        ax.set_xticks(chart_data['price_date_stats'])  # Set x-ticks to be the actual data points
        ax.set_yticks(chart_data['product_price_stats'])  # Set y-ticks to be the actual data points
        st.pyplot(fig)
    except Exception as e:
        st.write(f"Error creating chart: {e}")
























if __name__ == '__main__':
    main()
