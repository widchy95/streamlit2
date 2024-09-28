
import plotly.express as px
import streamlit as st
import pandas as pd
# Load the dataset
df = pd.read_csv(r'C:\Users\jwidc\Downloads\municipal_demographics.csv')
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")
csv = convert_df(df)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="population.csv",
    mime="text/csv",
)
# Add a multiselect box for selecting gender
selected_genders = st.multiselect(
    'Select Gender',
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)
# Filter the DataFrame based on the selected genders
df_filtered = df[df['Gender'].isin(selected_genders)]
# Group by city and gender, then calculate the average income
df_avg_income = df_filtered.groupby(['City', 'Gender'], as_index=False)['Income'].mean()
# Create the Plotly bar chart
fig = px.bar(df_avg_income, x='City', y='Income', color='Gender',
             title="Average Income per City and Gender", barmode='group')
# Display the chart in Streamlit
st.plotly_chart(fig)