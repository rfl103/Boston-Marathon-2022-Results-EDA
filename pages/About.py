import streamlit as st

st.set_page_config(page_title="About This Data",
                   layout="wide")
st.title("2022 Boston Marathon Data")

st.write("This data was obtained from [Boston Marathon Results](http://registration.baa.org/2022/cf/Media/iframe_ResultsSearch.cfm?mode=entry).")

st.image("images/jacob-licht-unsplash.jpg")
st.caption("Image courtesy of Jacob Licht via unsplash.")