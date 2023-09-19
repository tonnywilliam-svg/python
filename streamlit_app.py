import streamlit as st
import pandas as pd

countries=['china', 'russia', 'korea-south', 'united-states']
options = st.multiselect(
    'Pick your countries',
    countries,default=countries)

if __name__ == '__main__':
    df0 = pd.read_csv('countries.csv')
    df0 = df0.drop(df0.columns[0],axis=1)
    df=df0.query("country in @options")
    df['amount']=df['amount'].str.replace('(male ','<br> m:')
    df['amount']=df['amount'].str.replace(r"/female (.+)\)", r"<br> f:\1", regex=True)
    table = pd.pivot(df, values='amount', index=['item', 'sub-item'], columns='country')
    st.markdown(table.to_html(escape=False), unsafe_allow_html=True)

