# ovm-bridges
analysing the lost funds in optimistic bridges

### Overview

This code is a dashboard on lost funds in Optimistic bridges throughout multiple OVM chains. We are using Chainbase SDK to extract withdrawals and deposits between L1 and L2 chains. The main goal is to collect data on initiated, proven, and finalized withdrawals, as well as deposits, then aggregate it for analysis in the Streamlit frontend.

It is surprising there are over 20,000 ETH stuck in this manner, and this number will continue increasing unless awareness is raised on the matter. As the rollup ecosystem grows, these forgotten funds will only get harder to claim back.

### Installation Steps
- ensure you have poetry installed. else, go to (https://python-poetry.org/docs/#installing-with-the-official-installer)[https://python-poetry.org/docs/#installing-with-the-official-installer].
- ensure you have poetry-dotenv-plugin:
   ```bash
   poetry self install poetry-dotenv-plugin
   ```
- install the dependencies
   ```bash
   poetry install
   ```
- ensure you can access the streamlit cli
- shell into the repository
   ```bash
   poetry shell
   ```
- set up the env file
   ```env
CHAINBASE_API_KEY="key"
THIRD_WEB_CLIENT_ID='key'
THIRD_WEB_SECRET_KEY='key-key'
   ```
- run the frontend file or the jupyter notebook

- if you are running jupyter, ensure your data folder (`./data/{L2_CHAIN}/`) exists to save CSV output files.

###
The app.py file is a Streamlit-based Python web application that serves as a dashboard to visualize transaction data from blockchain networks. The dashboard is to be designed to display information such as:

Transaction Volumes: Shows the volume of deposits, withdrawals, and the balance of assets on different blockchain layers (Layer 2 solutions).
Chain Selection: Allows users to filter the data based on specific chains (e.g., "All chains," "Base," "Optimism").
Web3 Integration: Connects to a Web3 wallet using the web3modal component, enabling blockchain interaction for authenticated users.
Data Visualization: Provides various charts and metrics, such as cumulative transaction volumes, unwithdrawn funds, and other daily metrics.