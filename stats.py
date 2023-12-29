import streamlit as st
import requests
import pandas as pd
import plotly.express as px

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
        fig = px.line(chart_data, x='price_date_stats', y='product_price_stats', 
                      labels={'price_date_stats':'Date', 'product_price_stats':'Price'}, 
                      title='Price History')
        fig.update_layout(
            autosize=False,
            width=500,
            height=500,
            plot_bgcolor='rgb(230, 230,230)',
            paper_bgcolor='rgb(230, 230,230)',
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.write(f"Error creating chart: {e}")

if __name__ == '__main__':
    main()
