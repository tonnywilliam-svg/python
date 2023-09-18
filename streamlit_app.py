import streamlit as st
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv("countries.csv")
    df = df.drop(df.columns[0],axis=1)
    df['amount']=df['amount'].str.replace('\(male.+$','',regex=True)
    table = pd.pivot(df, values='amount', index=['item', 'sub-item'], columns='country')
    st.dataframe(table, use_container_width=True)

