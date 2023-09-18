import streamlit as st
import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv("csv_practice.csv")
    st.table(data)
