import streamlit as st
from pandas import read_csv, read_excel, read_table
from seaborn import load_dataset

from user_interface.ui import Selectbox, File_uploader

file_extensions = {'read_csv': read_csv,
                   'read_table': read_table,
                   'read_excel': read_excel
                   }

data_sources = {'iris': load_dataset(
    "iris"), 'penguins': load_dataset("penguins")}
files = file_extensions.keys()
data = data_sources.keys()

def Sidebar(expander=True):
    def index():
        Selectbox("select library", ["pandas", "pyspark"])
        Selectbox("data source", ["default dataset", "upload data"])
        if st.session_state['data_source'] == "upload data":
            Selectbox(lbl="file type", options=files)
            file = File_uploader("upload data", type=files)
            if file:
                df = file_extensions[st.session_state['file_type']]
            else:
                df = data_sources['iris']
        else:
            Selectbox("select data", options=data)
            df = data_sources[st.session_state['select_data']]
        st.session_state['df'] = df

    #expander
    if expander:
        with st.sidebar:
            with st.expander("configure dataset"):
                index()
    else:
        with st.sidebar:
            index()