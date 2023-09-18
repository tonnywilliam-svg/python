import streamlit as st
import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv("countries.csv",index_col=1)
    st.table(data)
