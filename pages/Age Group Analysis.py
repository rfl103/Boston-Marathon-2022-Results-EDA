import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Age Group Analysis of Results")

st.write("An interesting aspect of the Boston marathon is that many runners must qualify for the race by beating a qualifying"
         "standard time that is set for each age group by the race organizers. Due to field size limitations, the standard that "
         "the runners must meet is often even lower than the standard published due to the high interest in participation.  "
         "Although this is part of what makes the race so prestigious, it does make qualifying for the race more difficult for runners.")
st.write("Although some athletes due qualify for the race through other means such as through raising money through charity, the "
         "majority of the field must meet these competitive standards.")
st.write("This page analyzes the results of the race in an attempt to determine if runners whose age is on the lower end of the "
         "age group are more likely to be competitive in the race or if they are more likely to make it into the race.")

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
    df['OfficialTime'] = pd.to_datetime(df['OfficialTime'], format='%H:%M:%S')
    return df

df = load_data("Runners_all_results.csv")

st.header("Official Finish Time by Age Group", divider='rainbow')
#Average finishing time by Age Group
avg_age_results = df.groupby(['Age Group','Gender'])['OfficialTime'].mean().reset_index()

#creating the scatter plot
fig = px.scatter(avg_age_results, x="Age Group", y="OfficialTime", color="Gender", title="Average Finishing Time by Age Group")

# Customize the time axis format
fig.update_layout(yaxis=dict(
    tickvals=[avg_age_results['OfficialTime'].min(), avg_age_results['OfficialTime'].max()],
    showticklabels=False
))

fig.update_traces(hovertemplate="Age Group: %{x}<br>Official Time: %{y| %H:%M:%S}<br>")

st.plotly_chart(fig, use_container_width=True)

st.write("It appears that average finishing time increases as age increases.  Males finishers also typically have a faster "
         "average finish time in most age groups with the exception of 80 and over.")

st.divider()

st.header("Do people on the lower end of each age group have an advantage?", divider='rainbow')
st.write("Filter the results by age group to further determine if finishers that were statistically on the lower end of each"
         "age group had an advantage being more likely to meet the qualifying time to enter the race.")

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

#aggregating data in filtered dataframe to show average time and total participation by age
age_stats_df = filtered_df.groupby('AgeOnRaceDay')['OfficialTime'].mean().reset_index()
age_stats_df.columns = ['AgeOnRaceDay', 'Average Official Time']

#creating the scatter plot
fig = px.scatter(age_stats_df, x="AgeOnRaceDay", y="Average Official Time", title="Average Finishing Time by Age (Within Age Group)")

# Customize the time axis format
fig.update_layout(yaxis=dict(
    tickvals=[age_stats_df['Average Official Time'].min(), avg_age_results['OfficialTime'].max()],
    showticklabels = False
))

fig.update_traces(hovertemplate="Age Group: %{x}<br>Official Time: %{y| %H:%M:%S}<br>")


st.plotly_chart(fig, use_container_width=True)
st.write("As I was reviewing the data, I noticed that 18-34 age group appears to be an anomoly in that participants that are younger tend to have higher finishing "
         "times. However, in most age groups it appears that younger participants in the age group tend to have faster finishing "
         "times.  This may indicate that those who are in the lower range to be included in each age group may be at an advantage"
         "in regards to qualifying for the race, but further study would be needed.")

st.subheader("Percentage of Finishers by Age in Age Group", divider='rainbow')

#pie chart of age distribution
age_dist = filtered_df["AgeOnRaceDay"].value_counts()
fig = px.pie(age_dist, values="count", names=age_dist.index, title="Finishers by Age in Designated Age Group")
st.plotly_chart(fig, use_container_width=True)

st.write("The pie chart above indicates the percentages of each age that makes up each age group and can be used to further"
         "examine the data.  This data supports the theory that more testing would be needed to verify that runners who are "
         "on the younger end of each age group are more likely to qualify as the youngest age included in each division "
         "does not always make up the greatest proportion of runners.")

st.write("This data also does not take into account finishers that entered the race through other qualification routes "
         "which does not appear to be publicly available.")

st.image("images/jenny-hill-unsplash.jpg")
st.caption("Image courtesy of Jenny Hill via unsplash.")