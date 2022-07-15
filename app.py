import streamlit as st
import pandas as pd

from components.sidebar import Sidebar
from components.descriptive_stats import descriptive_statistics
from components.data_manipulation import data_manipulation
from components.function_application import function_application

# page configuration
st.set_page_config(page_title="Data manipulation", page_icon=None, layout="wide",
                   initial_sidebar_state="auto", menu_items=None)

def set_columns():
    options = []
    options.extend(list(st.session_state['df'].columns))
    st.session_state['columns'] = options


def main():
    Sidebar()
    set_columns()    
    descriptive_statistics()
    data_manipulation()
    function_application()



if __name__ == '__main__':
    main()

