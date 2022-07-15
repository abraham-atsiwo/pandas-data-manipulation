import streamlit as st 
from user_interface.ui import Selectbox, Multiselect


def descriptive_statistics():
    with st.expander("Computations / descriptive statistics"):
        val = Selectbox("descriptive statistics", options=["describe"])
        options = st.session_state['columns']
        columns = ['all']
        columns.extend(options)
        Multiselect("select columns", options=columns)
        if st.session_state['df'] is not None:
            df = st.session_state['df']
            if st.session_state['descriptive_statistics'] == 'describe':
                selected_col = st.session_state['select_columns']
                if selected_col != []:
                    if 'all' in selected_col:
                        col = st.session_state['columns']
                    else:
                        col = list(st.session_state['select_columns'])
                    df = df[col]
                    output = df.describe()
                    st.write(output)
