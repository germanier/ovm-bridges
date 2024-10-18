import streamlit as st
import pandas as pd


data_withdraw = {
    'block_number_started': [2916157, 2916189, 2916199, 2916284],
    'block_timestamp_started': [
        '2023-08-21 12:41:01',
        '2023-08-21 12:42:05',
        '2023-08-21 12:42:25',
        '2023-08-21 12:45:15'
    ],
    'transaction_hash_started': [
        '0x32a62eae09bed91025343fa39c0466ba1ee92cb894cb6dad68573a291cf54994',
        '0xf83863a1257e58c7bc485bae8e78ceb7c5eb20071b6c6509cba3bd9c242e79cb',
        '0x3901fa18a44b42b65469280ee61fa7f47cafbd996b286852764f679a25c9536a',
        '0x82f6f31771e7572fa4a9562290a63c886af531f4c6c1381e288ccbb84e52c557'
    ],
    'event_started': ['SentMessage'] * 4,
    'signature_started': [
        'MessagePassed(uint256,address,address,uint256,uint256,bytes,bytes3,1766847064778384329583297500742918515827483896875618958121606201292634470',
        'MessagePassed(uint256,address,address,uint256,uint256,bytes,bytes3,1766847064778384329583297500742918515827483896875618958121606201292634471',
        'MessagePassed(uint256,address,address,uint256,uint256,bytes,bytes3,1766847064778384329583297500742918515827483896875618958121606201292634472',
        'MessagePassed(uint256,address,address,uint256,uint256,bytes,bytes3,1766847064778384329583297500742918515827483896875618958121606201292634473'
    ],
    'nonce': [None] * 4,
    'sender': [
        '0xe35e388f10bc1f43506603a2ac9bf168ab5c6c09',
        '0x676fb89b3c64db5853046dc66eae6312de558dc6',
        '0x594a1a7e8d5c39a92218980bbd62db5fe099d9d9',
        '0xe7802d58698e0f69219b82e140208fc2108fbfbb'
    ],
    'target': [
        '0xe35e388f10bc1f43506603a2ac9bf168ab5c6c09',
        '0x676fb89b3c64db5853046dc66eae6312de558dc6',
        '0x594a1a7e8d5c39a92218980bbd62db5fe099d9d9',
        '0xe7802d58698e0f69219b82e140208fc2108fbfbb'
    ],
    'value': [
        10000000000000000,
        68310000000000000,
        73458000000000000,
        25000000000000000
    ],
    'withdrawal_hash': [
        '0x9a60475be6c63dcff09cb7cb28be8555b9376768f362bf5ec7473302cd579895',
        '0x1c5b7f9c25a0f4dad4fcd4c7e4a42d6bd46a601152955af9ef18506bae10a584',
        '0xb4e1a41906721c526f1330c157e6ca9d1c14cfab5dc18d71d7db43b1fb3a38a0',
        '0x4506dbfd8611ac4f4eb94f72c51cae5dd03b49ffe11b9974cf2cf12c04c004c0'
    ],
    'block_number_proven': [None] * 4,
    'block_timestamp_proven': [None] * 4,
    'transaction_hash_proven': [None] * 4,
    'method_id': [None] * 4,
    'event_proven': [None] * 4,
    'signature_proven': [None] * 4,
    'block_number': [None] * 4,
    'block_timestamp': [None] * 4,
    'transaction_hash': [None] * 4,
    'method_id_finalized': [None] * 4,
    'event': [None] * 4,
    'signature': [None] * 4
}
csv_withdrawal = 'data/base/base_withdrawals.csv'
data_withdraw = pd.read_csv(csv_withdrawal)
#data_withdraw = pd.DataFrame(data_withdraw)

data_withdraw['value'] = pd.to_numeric(data_withdraw['value'], errors='coerce')
data_withdraw['block_timestamp'] = pd.to_datetime(data_withdraw['block_timestamp'], errors='coerce')
data_withdraw['value_normalized'] = data_withdraw['value']/1e18

csv_deposit = 'data/base/base_deposits.csv'
data_deposit = pd.read_csv(csv_deposit)
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
    text_input1 = st.text_input('Wallet address', '')
    st.write("")
    st.divider()
    st.write("")
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
col1, col2, col3, col4 = st.columns(4) # overrides
with col1:
    st.write(f'**Volume in**\n\n{data_deposit['msg_value_normalized'].sum():,.2f} Ξ')
    st.write("")
    st.divider()
    st.write("")
with col2:
    st.write(f'**Volume out**\n\n{data_withdraw['value_normalized'].sum():,.2f} Ξ')
    st.write("")
    st.divider()
    st.write("")
with col3:
    st.write(f'**Volume to prove**\n\n{'how do I compute it?'}')
    st.write("")
    st.divider()
    st.write("")
with col4:
    st.write(f'**Volume to withdraw**\n\n{(
        data_deposit['msg_value_normalized'].sum() -
        data_withdraw['value_normalized'].sum()):,.2f}')
    st.write("")
    st.divider()
    st.write("")

st.write("")
st.divider() # decide if u want this one or each one below every column
st.write("")

# VISUALIZATION SECTION
st.subheader('Visualization')

daily_aggregate_deposit = data_deposit.copy()
data_deposit['daily_count'] = daily_aggregate_deposit.groupby('block_timestamp').transform('size')
daily_aggregate_deposit = data_deposit.groupby(pd.Grouper(key='block_timestamp', freq='D')).sum().reset_index()
daily_aggregate_deposit = daily_aggregate_deposit[['block_timestamp', 'msg_value_normalized', 'daily_count']]
#last_365_days = pd.Timestamp.now().normalize() - pd.DateOffset(days=365)
#filtered_df = daily_aggregate_deposit[daily_aggregate_deposit['block_timestamp'] >= last_365_days]
st.line_chart(daily_aggregate_deposit.set_index('block_timestamp')[['msg_value_normalized', 'daily_count']])

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
