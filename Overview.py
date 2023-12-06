import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Boston Marathon 2022 Results",
                   layout="wide")

#loading data
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv, encoding='latin-1')
    return df

df = load_data("Runners_all_results.csv")

st.title("Boston Marathon 2022 Results Exploratory Data Analysis")

st.write("The Boston Marathon is an annual marathon hosted by several cities/towns in the greater Boston, Massachusetts area. "
         "The event is one of the 6 current World Marathon Majors and is an extremely prestigious event in the running world. "
         "The 2022 Boston Marathon was held on Patriots' Day, April 18, 2022.  This was the 126th official running of the event.")

#Overall Winners
st.header("Overall Winners", divider='rainbow')
a1,a2 = st.columns(2)
with a1:
    st.metric("Overall Male Winner: Evans Chebet", "2:06:51", label_visibility="visible")

with a2:
    st.metric("Overall Male Winner: Peres Jepchirchir", "2:21:01", label_visibility="visible")

#Quick Facts
st.header("Quick Facts", divider='rainbow')

b1,b2 = st.columns(2)
with b1:
    st.metric("Total Number of Finishers", len(df["FullName"]), label_visibility="visible")
with b2:
    st.metric("Average Finisher Age", round(df["AgeOnRaceDay"].mean(), 2), label_visibility="visible")

fig = px.box(df, y='Gender', x="AgeOnRaceDay", title="Age Distribution of 2022 Boston Marathon Finishers by Gender")
st.plotly_chart(fig)


#American finishers
st.header("American Runners", divider='rainbow')

st.subheader("Top Americans")

c1,c2 = st.columns(2)
with c1:
    top_american_male = df.query('Gender=="M" & CountryOfCtzName =="United States of America" ')
    st.metric("Top American Male", top_american_male["OfficialTime"].min(), label_visibility="visible")
with c2:
    top_american_female = df.query('Gender=="F" & CountryOfCtzName =="United States of America" ')
    st.metric("Top American Female", top_american_female["OfficialTime"].min(), label_visibility="visible")

#calculating number of finishers by US state
american_finishers = df[(df['CountryOfCtzName'] == "United States of America")]
state_data = american_finishers["StateName"].value_counts().reset_index()
top_20_state_data = state_data.nlargest(n=20, columns='count', keep="all")

#scatter plot showing 20 states with the most finishers
fig = px.bar(top_20_state_data,
                    x="StateName",
                    y="count",
                    title="Top 20 States With the Most Finishers")
st.plotly_chart(fig, use_container_width=True)

#International finishers
st.subheader("International Runners", divider='rainbow')

d1, d2, d3 = st.columns(3)
with d1:
    num_of_inter = len(df[df["CountryOfCtzName"]!="United States of America"])
    st.metric("Number of International Finishers", num_of_inter, label_visibility="visible")
with d2:
    num_of_countries= len(df["CountryOfCtzName"].unique())
    st.metric("Number of Countries Represented", num_of_countries, label_visibility="visible")

#calculating number of international finisher per country
inter_finishers = df[(df['CountryOfCtzName'] != "United States of America")]
inter_data = inter_finishers["CountryOfCtzName"].value_counts().reset_index()
top_20_inter_data = inter_data.nlargest(n=20, columns='count', keep="all")

#scatter plot showing 20 countries with the most finishers
fig = px.bar(top_20_inter_data,
                    x="CountryOfCtzName",
                    y="count",
                    title="Top 20 Countries With the Most Finishers")
st.plotly_chart(fig, use_container_width=True)

#Image
st.image("images/miguel-a-amutio-unsplash.jpg")
st.caption("Runners running in a marathon. Image courtesy of Miguel A Amutio via Unsplash.")
