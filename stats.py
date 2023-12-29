import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Set page to use wide layout
st.set_page_config(layout="wide")

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

    # Calculate highest price, lowest price, and average price
    highest_price = chart_data['product_price_stats'].max()
    lowest_price = chart_data['product_price_stats'].min()
    average_price = chart_data['product_price_stats'].mean()

    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_data['price_date_stats'], y=chart_data['product_price_stats'], mode='lines+markers', 
                                 name='Price History', line=dict(color='#FF9900')))
        
        # Add a horizontal line for the average price
        fig.add_shape(type="line",
                      x0=chart_data['price_date_stats'].min(), y0=average_price,
                      x1=chart_data['price_date_stats'].max(), y1=average_price,
                      line=dict(color="RoyalBlue",width=2))
        
        # Add a red dot for the highest price
        fig.add_trace(go.Scatter(x=[chart_data['price_date_stats'].iloc[np.argmax(chart_data['product_price_stats'])]], 
                                 y=[highest_price], mode='markers', 
                                 marker=dict(color='Red', size=10), name='Highest Price'))
        
        # Add a green dot for the lowest price
        fig.add_trace(go.Scatter(x=[chart_data['price_date_stats'].iloc[np.argmin(chart_data['product_price_stats'])]], 
                                 y=[lowest_price], mode='markers', 
                                 marker=dict(color='Green', size=10), name='Lowest Price'))
        
        fig.update_layout(title='Price History', xaxis_title='Date', yaxis_title='Price', autosize=True, 
                          template='plotly_dark', title_x=0.5, font=dict(size=18))
        fig.update_xaxes(tickfont=dict(size=16))  # Increase x-axis tick label size
        fig.update_yaxes(tickfont=dict(size=16))  # Increase y-axis tick label size
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.write(f"Error creating chart: {e}")

if __name__ == '__main__':
    main()
