import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Boston Marathon 2022 Results",
                   layout="wide")

#loading data
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv, encoding='latin-1')

    # calculating age groups
    age_groups = []

    for value in df["AgeOnRaceDay"]:
        if value <= 34:
            age_groups.append("18-34")
        elif value <= 39:
            age_groups.append("35-39")
        elif value <= 44:
            age_groups.append("40-44")
        elif value <= 49:
            age_groups.append("45-49")
        elif value <= 54:
            age_groups.append("50-54")
        elif value <= 59:
            age_groups.append("55-59")
        elif value <= 64:
            age_groups.append("60-64")
        elif value <= 69:
            age_groups.append("65-69")
        elif value <= 74:
            age_groups.append("70-74")
        elif value <= 79:
            age_groups.append("75-79")
        else:
            age_groups.append("80 and over")

    df["Age Group"] = age_groups

    return df

df = load_data("Runners_all_results.csv")

#Female Participation
st.header("Female Participation", divider='rainbow')
st.write("Women were not allowed to officially register as marathon participants until 1971.  In recent years, the number of "
         "female participants in road racing has increased.  This page examines female participation in the 2022 Boston Marathon.")

st.subheader("Number of Male vs Female Finishers", divider='rainbow')
#metrics
a1,a2 = st.columns(2)
with a1:
    st.metric("Male Finishers", value = len(df[df["Gender"] == "M"]))
with a2:
    st.metric("Female Finishers", value=len(df[df["Gender"] == "F"]))

#pie chart of gender distribution
gender_dist = df["Gender"].value_counts()
fig = px.pie(gender_dist, values="count", names=gender_dist.index, title="Finishers by Gender in the 2022 Boston Marathon")
st.plotly_chart(fig, use_container_width=True)

st.write("Although the number of female finishers has certainly risen throughout the years, there were more male finishers"
         "in comparison to female finishers in the 2022 marathon.  It will be interesting to see if this breakdown changes over the coming years.")

st.subheader("Comparison of Male and Female Finishers by Age Group", divider='rainbow')
#Finishers by Age and Gender
gender_age_groupings = df.groupby(['Gender', 'Age Group']).size().reset_index(name='Count')

fig = px.bar(
    gender_age_groupings,
    x = 'Age Group',
    y='Count',
    color='Gender',
    barmode='group',
    labels={'AgeOnRaceDay': 'Age Group', 'Count': 'Number of Runners'},
    title='Comparison of Males and Females by Age Group'
)
st.plotly_chart(fig, use_container_width=True)

st.write("Interestingly, it appears that there are more women than men in the '18-34' age group. However, this is not the "
         "case in the age groups for older runners.  It will be interesting to see if this trend changes in the coming years as "
         "women in the '18-34' age group age into other age groups.")

st.image("images/andrew-tanglao-unsplash.jpg")
st.caption("Image courtesy of Andrew Tanglao via unsplash.")
