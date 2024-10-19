import streamlit as st
import pandas as pd
import web3modal
import os

THIRD_WEB_SECRET_KEY='Nm1d9IwC_8KH_wqcWHF52zsiZ0J9vlhvbJ98oKweNZzpmsTOPt9BwCIUWlxPY'
print(THIRD_WEB_SECRET_KEY)

# IMPORT AND PREPARE DATA
data_withdraw = pd.read_csv('data/base/base_withdrawals.csv')
data_withdraw['value'] = pd.to_numeric(data_withdraw['value'], errors='coerce')
data_withdraw['block_timestamp_started'] = pd.to_datetime(data_withdraw['block_timestamp_started'], errors='coerce')
data_withdraw['value_normalized'] = data_withdraw['value']/1e18

data_deposit = pd.read_csv('data/base/base_deposits.csv')
data_deposit['block_timestamp'] = pd.to_datetime(data_deposit['block_timestamp'], errors='coerce')
data_deposit['msg_value_normalized'] = data_deposit['msg_value']/1e18



st.title("Volume dashboard")

st.write("")
st.divider()
st.write("")



# INPUT SECTION
st.subheader('Select wallet or chain')
# Create two columns for the text input boxes
col1, col2 = st.columns(2)
# First input box in the first column
with col1:
    #text_input1 = st.text_input('Wallet address', '')
    st.write('Wallet')
    btn = st.button("Click me")
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

# Second input box in the second column
with col2:
    select_option = st.selectbox(
        'Chain', 
        ['All chains', 'Chain 1', 'Chain 2', 'Chain 3']
    )


st.write("")
st.divider()
st.write("")


# SUMMAY SECTION
st.subheader('Counters')

L2_balance = data_deposit['msg_value_normalized'].sum() - data_withdraw['value_normalized'].sum()
volume_notApproved = data_withdraw.loc[data_withdraw['transaction_hash_proven'].isna(), 'value_normalized'].sum()
volume_notFinalized = data_withdraw.loc[data_withdraw['transaction_hash_finalized'].isna(), 'value_normalized'].sum()

col1, col2, col3 = st.columns(3) # overrides
with col1:
    st.write(f'**Volume in**\n\n{data_deposit['msg_value_normalized'].sum():,.2f} Ξ')
    st.write("")
with col2:
    st.write(f'**Volume out**\n\n{data_withdraw['value_normalized'].sum():,.2f} Ξ')
    st.write("")
with col3:
    st.write(f'**L2 balance**\n\n{(L2_balance):,.2f} Ξ')
    st.write("")

col1, col2 = st.columns(2)
with col1:
    st.write(f'**Volume to prove**\n\n{volume_notApproved:,.2f} Ξ')
    st.write("")
    st.divider()
    st.write("")
with col2:
    st.write(f'**Volume to withdraw**\n\n{volume_notFinalized:,.2f} Ξ')
    st.write("")
    st.divider()
    st.write("")


# VISUALIZATION SECTION
st.subheader('Visualization')

daily_aggregate_deposit = data_deposit.copy()
data_deposit['daily_count'] = daily_aggregate_deposit.groupby('block_timestamp').transform('size')
daily_aggregate_deposit = data_deposit.groupby(pd.Grouper(key='block_timestamp', freq='D')).sum().reset_index()
daily_aggregate_deposit = daily_aggregate_deposit[['block_timestamp', 'msg_value_normalized', 'daily_count']]
#last_365_days = pd.Timestamp.now().normalize() - pd.DateOffset(days=365)
#filtered_df = daily_aggregate_deposit[daily_aggregate_deposit['block_timestamp'] >= last_365_days]
st.write("Deposits")
st.area_chart(daily_aggregate_deposit.set_index('block_timestamp')[['daily_count','msg_value_normalized']])

col1, col2 = st.columns(2)
# First input box in the first column
with col1:
    last_7_days = pd.Timestamp.now().normalize() - pd.DateOffset(days=30) # set as 7 pliz
    deposit_last7days = daily_aggregate_deposit[daily_aggregate_deposit['block_timestamp'] >= last_7_days]
    st.write(f'**Bridgers last 7 days**\n\n{deposit_last7days['daily_count'].sum():,.2f}')
    st.write(f'**TVB last 7 days**\n\n{deposit_last7days['msg_value_normalized'].sum():,.2f} Ξ')
with col2:
    last_year = pd.Timestamp.now().normalize() - pd.DateOffset(days=365) # set as 7 pliz
    deposit_lastyear = daily_aggregate_deposit[daily_aggregate_deposit['block_timestamp'] >= last_year]
    st.write(f'**Bridgers last year**\n\n{deposit_lastyear['daily_count'].sum():,.2f}')
    st.write(f'**TVB last year**\n\n{deposit_lastyear['msg_value_normalized'].sum():,.2f} Ξ')

st.write("")
st.write("")
st.write("")
st.write("Withdrawals cumulative")
data_withdraw["value_notProven"] = data_withdraw.apply(lambda x: x['value_normalized'] if pd.isna(x['transaction_hash_proven']) else 0, axis=1)
data_withdraw["value_notFinalized"] = data_withdraw.apply(lambda x: x['value_normalized'] if pd.isna(x['transaction_hash_finalized']) else 0, axis=1)
daily_aggregate_withdraw = data_withdraw.groupby(pd.Grouper(key='block_timestamp_started', freq='D')).sum().reset_index()
daily_aggregate_withdraw = daily_aggregate_withdraw[['block_timestamp_started', 'value_normalized', 'value_notProven', 'value_notFinalized']]
#last_365_days = pd.Timestamp.now().normalize() - pd.DateOffset(days=365)
#filtered_df = daily_aggregate_deposit[daily_aggregate_deposit['block_timestamp'] >= last_365_days]
daily_aggregate_withdraw['cumulative_value'] = daily_aggregate_withdraw['value_normalized'].cumsum()
daily_aggregate_withdraw['cumulative_notProven'] = daily_aggregate_withdraw['value_notProven'].cumsum()
daily_aggregate_withdraw['cumulative_notFinalized'] = daily_aggregate_withdraw['value_notFinalized'].cumsum()
st.area_chart(daily_aggregate_withdraw.set_index('block_timestamp_started')[['cumulative_value', 'cumulative_notFinalized', 'cumulative_notProven']])
