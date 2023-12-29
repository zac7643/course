
import streamlit as st
import pip._vendor.requests as requests
import pandas as pd
import matplotlib.pyplot as style
import matplotlib.pyplot as plt
import numpy as np


import matplotlib.style as style

def main():
    st.title('Price History')
    response = requests.get('http://141.147.64.158/getstatschart/')
    content = response.text.strip()

    try:
        data = response.json()
        chart_data = pd.DataFrame(data)
        chart_data = chart_data[['product_price_stats', 'price_date_stats']]
        chart_data['product_price_stats'] = chart_data['product_price_stats'].astype(float)
        chart_data['price_date_stats'] = pd.to_datetime(chart_data['price_date_stats']).dt.date
        chart_data.sort_values('price_date_stats', inplace=True)
    except Exception as e:
        st.write(f"Error: {str(e)}")
        return

    try:
        style.use('ggplot')  # Use the 'ggplot' style
        fig, ax = plt.subplots()
        ax.plot(chart_data['price_date_stats'], chart_data['product_price_stats'], marker='o')
        ax.set_xticks(chart_data['price_date_stats'])
        ax.set_yticks(chart_data['product_price_stats'])
        plt.title('Price History', fontsize=20)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Price', fontsize=14)
        st.pyplot(fig)
    except Exception as e:
        st.write(f"Error creating chart: {e}")

if __name__ == '__main__':
    main()
