import streamlit as st
import pandas as pd
import web3modal
import os

THIRD_WEB_SECRET_KEY = '3dcd8b35413c144b8f25805a1179db22'
#print(THIRD_WEB_SECRET_KEY)

# IMPORT AND PREPARE DATA
data_withdraw = pd.read_csv('data/base/basic_withdrawals.csv')
data_deposit = pd.read_csv('data/base/basic_deposits.csv')
data_counters = pd.read_csv('data/base/counters.csv')
data_daily = pd.read_csv('data/base/daily_volumes.csv')
data_forgotten = pd.read_csv('data/base/forgotten_funds.csv')

st.title("Volume dashboard")

st.write("")
st.divider()
st.write("")

with st.sidebar.header("Web3Modal"):
    st.write('Wallet')
    btn = st.button("Confirm connection")
    with st.sidebar.header("Web3Modal"):
        connect_button = st.connect_component(key=THIRD_WEB_SECRET_KEY, modal_size="wide")
        if isinstance(connect_button, dict) and connect_button["address"] != "None":
            st.session_state['address'] = connect_button["address"]
                # Display the address from the session state
    if btn:
        if 'address' in st.session_state:
            st.write('Connected!')
            st.write(st.session_state['address'])
        else:
            st.write('Not Connected!')
    
with st.sidebar:
    select_option = st.selectbox(
        'Chain', 
        ['All chains', 'Base', 'Optimism']
    )


# SUMMAY SECTION
st.subheader('Counters')

col1, col2, col3 = st.columns(3) # overrides
with col1:
    st.write(f'**Volume in**\n\n{data_daily['deposited_volume'].sum():,.2f} Ξ')
    st.write("")
with col2:
    st.write(f'**Volume out**\n\n{data_daily['initiated_volume'].sum():,.2f} Ξ')
    st.write("")
with col3: 
    st.write(f'**L2 balance**\n\n{data_daily['daily_difference'].sum():,.2f} Ξ')
    st.write("")

col1, col2 = st.columns(2)
with col1:
    st.write(f'**Volume to prove**\n\n{data_counters['sum_if_proven_null'].sum():,.2f} Ξ')
    st.write("")
with col2:
    st.write(f'**Volume to withdraw**\n\n{data_counters['sum_if_finalized_null'].sum():,.2f} Ξ')
    st.write("")


st.write("")
st.divider()
st.write("")


# VISUALIZATION SECTION
st.subheader('Visualization')

#col1, col2 = st.columns(2)
# First input box in the first column
#with col1:
#    last_7_days = pd.Timestamp.now().normalize() - pd.DateOffset(days=7) # set as 7 pliz
#    deposit_last7days = daily_aggregate_deposit[daily_aggregate_deposit['block_timestamp'] >= last_7_days]
#    st.write(f'**Bridgers last 7 days**\n\n{deposit_last7days['daily_count'].sum():,.2f}')
#    st.write(f'**TVB last 7 days**\n\n{deposit_last7days['value'].sum():,.2f} Ξ')
#with col2:
#    last_year = pd.Timestamp.now().normalize() - pd.DateOffset(days=365) # set as 7 pliz
#    deposit_lastyear = daily_aggregate_deposit[daily_aggregate_deposit['block_timestamp'] >= last_year]
#    st.write(f'**Bridgers last year**\n\n{deposit_lastyear['daily_count'].sum():,.2f}')
#    st.write(f'**TVB last year**\n\n{deposit_lastyear['value'].sum():,.2f} Ξ')

st.write("Cumulative transactions")
st.area_chart(data_daily.set_index('date')[['cumulative_deposited','cumulative_initiated', 'cumulative_proved', 'cumulative_finalized']])

st.write("Forgotten funds")
data_forgotten = data_forgotten.sort_values('date')
data_forgotten['cumulative_notWithdrawn'] = data_forgotten['total_not_withdrawn'].cumsum()
st.line_chart(data_forgotten.set_index('date')[['cumulative_notWithdrawn']])
