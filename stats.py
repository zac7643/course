import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Set page to use wide layout
st.set_page_config(layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #FF9900;'>Price History</h1>", unsafe_allow_html=True)

    try:
        response = requests.get('http://141.147.64.158/getstatschart/')
        data = response.json()
    except Exception as e:
        st.write(f"Error fetching data: {str(e)}")
        return

    try:
        chart_data = pd.DataFrame(data)
        chart_data = chart_data[['product_price_stats', 'price_date_stats']]
        chart_data['product_price_stats'] = chart_data['product_price_stats'].astype(float)
        chart_data['price_date_stats'] = pd.to_datetime(chart_data['price_date_stats']).dt.date
        chart_data.sort_values('price_date_stats', inplace=True)
    except Exception as e:
        st.write(f"Error processing data: {str(e)}")
        return

    # Calculate highest price, lowest price, and average price
    highest_price = chart_data['product_price_stats'].max()
    lowest_price = chart_data['product_price_stats'].min()
    average_price = chart_data['product_price_stats'].mean()

    # Calculate the standard deviation, which is a measure of how spread out the prices are
    std_dev = chart_data['product_price_stats'].std()

    try:
        fig = go.Figure()

        # Add the price history line
        fig.add_trace(go.Scatter(x=chart_data['price_date_stats'], y=chart_data['product_price_stats'], mode='lines+markers', 
                                 name='Price History', line=dict(color='#FF9900')))

        # Add a shaded area that represents the most common prices (within one standard deviation of the average)
        fig.add_trace(go.Scatter(
            x=chart_data['price_date_stats'].tolist() + chart_data['price_date_stats'].tolist()[::-1],  # x, then x reversed
            y=(chart_data['product_price_stats'] + std_dev).tolist() + (chart_data['product_price_stats'] - std_dev).tolist()[::-1],  # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(0,0,255,0.2)',  # semi-transparent fill
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ))

        # Add a red dot for the highest price
        fig.add_trace(go.Scatter(x=[chart_data['price_date_stats'].iloc[np.argmax(chart_data['product_price_stats'])]], 
                                 y=[highest_price], mode='markers', 
                                 marker=dict(color='Red', size=10), name='Highest Price'))

        # Add a green dot for the lowest price
        fig.add_trace(go.Scatter(x=[chart_data['price_date_stats'].iloc[np.argmin(chart_data['product_price_stats'])]], 
                                 y=[lowest_price], mode='markers', 
                                 marker=dict(color='Green', size=10), name='Lowest Price'))

        fig.update_layout(title='Price History', xaxis_title='Date', yaxis_title='Price', autosize=True, 
                          template='plotly_dark', title_x=0.5, 
                          font=dict(size=20),  # Increase size of title and axes labels
                          xaxis=dict(title_font=dict(size=20)),  # Increase x-axis title size
                          yaxis=dict(title_font=dict(size=20)))  # Increase y-axis title size
        fig.update_xaxes(tickfont=dict(size=18))  # Increase x-axis tick label size
        fig.update_yaxes(tickfont=dict(size=18))  # Increase y-axis tick label size
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.write(f"Error creating chart: {e}")

    # Display highest price, lowest price, and average price below the chart
    st.markdown(f"<h3 style='text-align: center; color: Red;'>Highest Price: <span style='color: Red;'>{highest_price}</span></h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: Green;'>Lowest Price: <span style='color: Green;'>{lowest_price}</span></h1>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
