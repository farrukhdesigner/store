# (1) Import the required libraries
import streamlit as st
import plotly.express as px
import pandas as pd

# (2) Page Configuration and Dashboard Title
st.set_page_config(page_title="Dashboard!!!", page_icon=":bar_chart:", layout="wide")
st.title("EDA of Superstore Data :bar_chart:")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# (3) Setting File Uploader Option on Dashboard
uploaded_file = st.file_uploader("Upload a File", type=["csv", "txt", "xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
    st.write(f"File '{uploaded_file.name}' uploaded successfully.")
else:
    default_data_path = r"C:\Users\hp\Google Drive\Fiverr Work\2023\57. Interactive Data Dashboard for Superstor Data (EDA)\Superstore.csv"
    df = pd.read_csv(default_data_path, encoding="ISO-8859-1")
    st.write("Using default data from:", default_data_path)

# (4) Selecting Date Range
col1, col2 = st.columns(2)
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Get the min and max date
startDate = df["Order Date"].min()
endDate = df["Order Date"].max()

# Create date input widgets
with col1:
    date1 = st.date_input("Start Date", startDate.date())  # Extract date part
with col2:
    date2 = st.date_input("End Date", endDate.date())  # Extract date part

# Convert date1 and date2 to datetime objects
date1 = date1 + pd.DateOffset(hours=0)  # Combine with time to get datetime
date2 = date2 + pd.DateOffset(hours=0)  # Combine with time to get datetime

# Filter the DataFrame based on the selected date range
df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)]

# (5) Set the filters option on the sidebar
st.sidebar.header("Choose your filter:")
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
state = st.sidebar.multiselect("Pick the State", df["State"].unique())
city = st.sidebar.multiselect("Pick the City", df["City"].unique())

# Filter the data based on Region, State, and City
filtered_df = df
if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]
if state:
    filtered_df = filtered_df[filtered_df["State"].isin(state)]
if city:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]

# (6) Create charts
category_df = filtered_df.groupby(by=["Category"], as_index=False)["Sales"].sum()
st.subheader("Category wise Sales")
fig = px.bar(category_df, x="Category", y="Sales", text=['${:,.2f}'.format(x) for x in category_df["Sales"]], template="seaborn")
st.plotly_chart(fig, use_container_width=True, height=300)

st.subheader("Region wise Sales")
fig = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
fig.update_traces(text=filtered_df["Region"], textposition="outside")
st.plotly_chart(fig, use_container_width=True, height=300)
