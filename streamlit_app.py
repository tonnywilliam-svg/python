import streamlit as st
import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv("countries.csv")
    st.table(data)
