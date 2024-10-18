import streamlit as st
import pandas as pd


st.title("Volume from L2 to L1 dashboard")

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


