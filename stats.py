import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

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

    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_data['price_date_stats'], y=chart_data['product_price_stats'], mode='lines+markers', 
                                 name='Price History', line=dict(color='#FF9900')))
        fig.update_layout(title='Price History', xaxis_title='Date', yaxis_title='Price', autosize=True, 
                          template='plotly_dark', title_x=0.5, font=dict(size=18))
        fig.update_xaxes(title_font=dict(size=30))  
        fig.update_yaxes(title_font=dict(size=30)) 
        fig.update_xaxes(tickfont=dict(size=16))
        fig.update_yaxes(tickfont=dict(size=16))  
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.write(f"Error creating chart: {e}")

if __name__ == '__main__':
    main()
