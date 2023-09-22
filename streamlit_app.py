import streamlit as st
import pandas as pd

st.set_page_config(page_title='hx streamlit',layout='wide')

df = pd.read_csv('countries.csv')
# some processing to shorten the data e.g. change (male: xxx) to m:xxx
df['amount']=df['amount'].str.replace('(male ','<br> m:')
df['amount']=df['amount'].str.replace(r"/female (.+)\)", r"<br> f:\1", regex=True)
df['sub_item']=df['sub_item'].str.replace(r":\s*$", r"", regex=True)  # remove the ending ":" from investment from consumption:

shortenings = (
    ("item","gdp-official-exchange-rate", "gdp"),
    ("item","gdp-composition-by-end-use", "gdp-by-end-use"),
    ("sub_item","investment in fixed capital", "inv"),
    ("sub_item","investment in inventories", "inventory"),
    ("sub_item","imports of goods and services", "import"),
    ("sub_item","exports of goods and services", "export"),
    ("sub_item","household consumption", "hh consumption"),
    ("sub_item","government consumption", "gov consumption")
)
for (column, replace_this, with_this) in shortenings:
    df[column]=df[column].str.replace(replace_this, with_this)

# set up multiselects for 3 columns: country, data item and sub item
options_country = st.multiselect(
    'Choose countries',
    countries :=df['country'].unique().tolist(),default=['china','united-states'])

options_item = st.multiselect(
    'Choose items',
    items :=df['item'].unique().tolist(), default=items)

options_sub_item = st.multiselect(
    'Choose sub items',
    sub_items :=df['sub_item'].unique().tolist(),default=sub_items)

df=df.query("country in @options_country and item in @options_item and sub_item in @options_sub_item")

table = pd.pivot(df, values='amount', index=['item', 'sub_item'], columns='country')
table = table.reindex(['age-structure','gdp-by-end-use','gdp'],level=0)
table = table.reindex(['0-14 years','15-64 years','65 years and over','hh consumption','gov consumption','inv','export','import','inventory','---'],level=1)

st.markdown(table.to_html(escape=False), unsafe_allow_html=True)

