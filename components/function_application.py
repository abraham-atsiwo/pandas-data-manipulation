import streamlit as st
from user_interface.ui import Selectbox, Multiselect

from numpy import array, mean, var, std
aggfunc = {'mean': mean,
                      'var': var,
                      'std': std,
                      'sum': sum,
                      'min': min, 
                      'max': max
                      }

def func(expander=True):
    cols = st.session_state['columns']
    def index():
        data = st.session_state['df']
        Multiselect(lbl='select_column', options=cols, key='select_column', default=cols[0])
        Multiselect(lbl="function", options=aggfunc.keys(), key="aggregate_func", default='mean')
        Selectbox(lbl="axis", options=['index', 'columns'], key="aggregate_axis")
        
        func = st.session_state['aggregate_func']
        axis = st.session_state['aggregate_axis']
        sel_col = st.session_state['select_column']
        if len(sel_col) > 0:
            data = data[sel_col]
        df = data.aggregate(func=func, axis=axis)
        st.dataframe(df)

    if expander:
        with st.expander("aggregate"):
            return index()
        return index

def function_application(expander=True):
    st.subheader("Function application, GroupBy & window")
    func(expander)