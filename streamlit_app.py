import streamlit as st
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv("countries.csv")
    df = df.drop(df.columns[0],axis=1)
    st.table(df)
