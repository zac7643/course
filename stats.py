import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #FF9900;'>Price History</h1>", unsafe_allow_html=True)

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

    # Calculate the interquartile range
    lower_quartile = np.percentile(chart_data['product_price_stats'], 25)
    upper_quartile = np.percentile(chart_data['product_price_stats'], 75)

    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_data['price_date_stats'], y=chart_data['product_price_stats'], mode='lines+markers', 
                                 name='Price History', line=dict(color='#FF9900')))
        
        # Add a shaded rectangle to represent the interquartile range
        fig.add_shape(
            type="rect",
            xref="x",
            yref="y",
            x0=chart_data['price_date_stats'].min(),
            y0=lower_quartile,
            x1=chart_data['price_date_stats'].max(),
            y1=upper_quartile,
            fillcolor="RoyalBlue",
            opacity=0.5,
            layer="below",
            line_width=0,
        )
        
        # Add a red dot for the highest price
        fig.add_trace(go.Scatter(x=[chart_data['price_date_stats'].iloc[np.argmax(chart_data['product_price_stats'])]], 
                                 y=[highest_price], mode='markers', 
                                 marker=dict(color='Red', size=10), name='Highest Price'))
        
        # Add a green dot for the lowest price
        fig.add_trace(go.Scatter(x=[chart_data['price_date_stats'].iloc[np.argmin(chart_data['product_price_stats'])]], 
                                 y=[lowest_price], mode='markers', 
                                 marker=dict(color='Green', size=10), name='Lowest Price'))
        
        fig.update_layout(title='', xaxis_title='Date', yaxis_title='Price', autosize=True, 
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
    st.markdown(f"<h5 style='text-align: center; color: Red;'>Highest Price: <span style='color: Red;'>{highest_price}</span></h1>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: center; color: Green;'>Lowest Price: <span style='color: Green;'>{lowest_price}</span></h1>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: center; color: RoyalBlue;'>Average Price: <span style='color: RoyalBlue;'>{average_price:.2f}</span></h1>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
