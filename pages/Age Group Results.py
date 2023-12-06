import streamlit as st
import pandas as pd

st.set_page_config(page_title="Age Group Results",
                   layout="wide")
st.title("Complete Results (Runners)")

st.write("Please filter the results using the sidebar to further examine the results sorted by age group and gender.")

#load data
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

#sidebar with filters
st.sidebar.header("Filter Results Here:")
gender = st.sidebar.selectbox(
    "Select Finisher's Gender:",
    df["Gender"].unique(),
    placeholder="Choose an option"
)

age = st.sidebar.selectbox(
    "Select Finisher's Age:",
    df["Age Group"].unique(),
    placeholder="Choose an option"
)

filtered_df = df.query(
    '`Gender` == @gender and `Age Group` == @age'
)

st.dataframe(filtered_df)
st.write("Please note: these results only include runners that completed the race. For results for the wheelchair and handcycle"
         "division, please visit [Boston Marathon Results](http://registration.baa.org/2022/cf/Media/iframe_ResultsSearch.cfm?mode=entry)")

