import streamlit as st
import pandas as pd

# --- User Input and Date ---

st.set_page_config(
    page_title="Budget Calculator",
    page_icon="💼",
    #initial_sidebar_state="collapsed",
)

# --- User Input and Date ---
user_name = st.text_input("Enter your name:", "Project Lead")
todays_date = st.date_input("Today's Date:")

# --- Cost Input Functions ---
def get_costs(cost_type):
    st.subheader(f"{cost_type} Costs")
    hourly_rate = st.number_input(f"Hourly {cost_type} Developer Rate ($)", value=96 if cost_type == "Onsite" else 35)
    overhead = st.number_input(f"{cost_type} Overhead Costs", value=0.0)
    return [hourly_rate, overhead]

# --- Project Scope ---
def get_project_scope():
    st.subheader("Project Scope")
    duration = st.number_input("Estimated Project Duration (weeks)", value=1)
    onsite_team_size = st.number_input("Onsite Team Size", value=1)
    offshore_team_size = st.number_input("Offshore Team Size", value=1)
    return {"duration": duration, "onsite_team_size": onsite_team_size, "offshore_team_size": offshore_team_size}

# --- Calculations ---
def calculate_budget(onsite_costs, offshore_costs, project_scope):
    total_onsite = sum(onsite_costs) * project_scope['duration'] * 40 * project_scope['onsite_team_size']
    total_offshore = sum(offshore_costs) * project_scope['duration'] * 40 * project_scope['offshore_team_size']
    return total_onsite, total_offshore

# --- Main App Logic --- 
st.sidebar.title("Budget Calculator (Onsite vs. Offshore)")  

onsite_costs = get_costs("Onsite")
offshore_costs = get_costs("Offshore")
project_scope = get_project_scope()

total_onsite, total_offshore = calculate_budget(onsite_costs, offshore_costs, project_scope)

# --- Display ---
st.subheader("Budget Summary")
st.metric("Total Onsite Cost", f"${total_onsite:,.2f}")
st.metric("Total Offshore Cost", f"${total_offshore:,.2f}")
st.metric("Total Overall Cost", f"${total_offshore+total_onsite:,.2f}")

# Chart (Example using Plotly)
import plotly.express as px
df = pd.DataFrame({'Cost Type': ['Onsite', 'Offshore'], 'Amount': [total_onsite, total_offshore]})
fig = px.bar(df, x='Cost Type', y='Amount', title="Budget Breakdown")
st.plotly_chart(fig)

# User and Date (Sidebar)
st.sidebar.subheader(f"Prepared by: {user_name}") 
st.sidebar.write(f"Date: {todays_date}") 
