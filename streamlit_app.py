import streamlit as st
import pandas as pd

st.set_page_config(page_title='hx streamlit',layout='wide')

df0 = pd.read_csv('countries.csv')
df=df0
# some processing to shorten the data e.g. change (male: xxx) to m:xxx
df['amount']=df['amount'].str.replace('(male ','<br> m:')
df['amount']=df['amount'].str.replace(r"/female (.+)\)", r"<br> f:\1", regex=True)
df['sub_item']=df['sub_item'].str.replace(r":\s*$", r"", regex=True)  # remove the ending ":" from investment from consumption:
# set up multiselect for 3 columns - country, data item and sub item
countries=df['country'].unique().tolist()
options_country = st.multiselect(
    'Choose countries',
    countries,default=['china','united-states'])

items=df['item'].unique().tolist()
options_item = st.multiselect(
    'Choose items',
    items, default=items)

sub_items=df['sub_item'].unique().tolist()
options_sub_item = st.multiselect(
    'Choose sub items',
    sub_items,default=sub_items)
# filter dataframe by 3 columns
df=df.query("country in @options_country and item in @options_item and sub_item in @options_sub_item")
# convert dataframe to table
table = pd.pivot(df, values='amount', index=['item', 'sub_item'], columns='country')
# show table
st.markdown(table.to_html(escape=False), unsafe_allow_html=True)
