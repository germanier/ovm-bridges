import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd

csv_file = 'data/base/base_deposits.csv'
data = pd.read_csv(csv_file)

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
    st.write(f'**Volume in**\n\n{'fake value Ξ'}')
    st.write("")
    st.divider()
    st.write("")
with col2:
    st.write(f'**Volume out**\n\n{'fake value Ξ'}')
    st.write("")
    st.divider()
    st.write("")
with col3:
    st.write(f'**Volume to prove**\n\n{'fake value Ξ'}')
    st.write("")
    st.divider()
    st.write("")
with col4:
    st.write(f'**Volume to withdraw**\n\n{'fake value Ξ'}')
    st.write("")
    st.divider()
    st.write("")

st.write("")
st.divider() # decide if u want this one or each one below every column
st.write("")

# VISUALIZATION SECTION
st.subheader('Visualization')
col1, col2 = st.columns(2)

try:
    with col1:
        st.write(f'**here goes piechart**\n\n{''}')

    with col2:
        if 'block_timestamp' in data.columns and 'msg_value' in data.columns:
            data['block_timestamp'] = pd.to_datetime(data['block_timestamp'], errors='coerce')

            # con
            data['msg_value_normalized'] = data['msg_value']/1e18

            # Group by day and aggregate the 'msg_value' column
            daily_aggregate = data.groupby(pd.Grouper(key='block_timestamp', freq='W')).sum().reset_index()

        if 'msg_value' in data.columns and 'block_timestamp' in data.columns:
            st.line_chart(daily_aggregate.set_index('block_timestamp')['msg_value_normalized'])
            print(daily_aggregate.head())
        else:
            st.write('Columns "block_number_started" and "block_timestamp" not found in the CSV.')

except FileNotFoundError:
    st.error(f'The file {csv_file} was not found. Please make sure the file exists in the specified location.')


