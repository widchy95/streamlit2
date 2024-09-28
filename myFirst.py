import plotly.express as px
import streamlit as st
import pandas as pd
# Load the dataset
df = pd.read_csv('municipal_demographics.csv')
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
# Add a slider to filter data based on Age
min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
age_range = st.slider(
    'Select Age Range',
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)
# Filter the DataFrame based on the selected age range
df_age_filtered = df_filtered[(df_filtered['Age'] >= age_range[0]) & (df_filtered['Age'] <= age_range[1])]
# Group by Age and Illness to get average income
df_age_income = df_age_filtered.groupby(['Age', 'Illness'], as_index=False)['Income'].mean()
# Create the Plotly scatter plot
fig_scatter = px.scatter(df_age_income,
                         x='Age',
                         y='Income',
                         color='Illness',
                         title="Average Income by Age and Illness")
# Display the scatter plot in Streamlit
st.plotly_chart(fig_scatter)
