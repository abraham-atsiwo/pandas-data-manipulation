import streamlit as st
from pandas import melt, pivot, pivot_table, crosstab, cut
from user_interface.ui import Selectbox, Multiselect
import numpy as np
from numpy import array, mean, var, std

pivotTable_aggfunc = {'mean': mean,
                      'var': var,
                      'std': std,
                      'sum': sum,
                      'min': min,
                      'max': max
                      }

def col_with_none():
    options = ['none']
    cols = st.session_state['columns']
    options.extend(cols)
    return options


def validate_col_value(val):
    if val == 'none':
        return None
    return val

def catch_exception(func):
    def wrapper(*args, **kwargs):
        try: 
            func(*args, **kwargs)
        except:
            error = "error processing function ..."
            st.write(error)
    return wrapper


def Melt(expander=True):
    cols = st.session_state['columns']
    data = st.session_state['df']

    def index():
        Multiselect(lbl="id_vars", options=cols, key="melt_id_vars")
        Multiselect(lbl="value_vars", options=cols, key="melt_value_vars")
        Selectbox(lbl="ignore_index", options=[
                  True, False], key="melt_ignore_index")
        df = melt(frame=data, id_vars=st.session_state['melt_id_vars'],
                  ignore_index=st.session_state['melt_ignore_index'],
                  value_vars=st.session_state['melt_value_vars'])
        st.dataframe(df)
    if expander:
        with st.expander("melt"):
            index()
    else:
        index()


def Pivot(expander=True):
    cols = st.session_state['columns']
    data = st.session_state['df']
    cols_none = col_with_none()

    def index():
        Selectbox(lbl="index", options=cols_none, key="pivot_index")
        Selectbox(lbl="columns", options=cols, key="pivot_columns")
        Multiselect(lbl="values", options=cols, key="pivot_values")
        columns = validate_col_value(st.session_state['pivot_columns'])
        index = validate_col_value(st.session_state['pivot_index'])
        values = validate_col_value(st.session_state['pivot_values'])
        try:
            df = pivot(
                data=data, columns=columns, index=index, values=values)
            st.dataframe(df)
        except ValueError as e:
            st.write(
                "The name sepal_length occurs multiple times, use a level number")
        except:
            st.write("Oops .....")
    if expander:
        with st.expander("pivot"):
            return index()
    return index()


def PivotTable(expander=True):
    cols = st.session_state['columns']
    data = st.session_state['df']
    cols_none = col_with_none()

    def index():
        aggfuncOpt = list(pivotTable_aggfunc.keys())
        Multiselect(lbl="index", options=cols,
                    key="pivotTable_index", default=cols[0])
        Selectbox(lbl="columns", options=cols_none, key="pivotTable_columns")
        Multiselect(lbl="values", options=cols_none,
                    key="pivotTable_values", default=cols[1])
        values = st.session_state['pivotTable_values']
        if len(values) > 0:
            st.write("aggfunc")
            for val in values:
                itemVal = 'values_'+val
                Multiselect(lbl=val, options=aggfuncOpt, default=aggfuncOpt[0],
                            key="pivotTable_aggfunc_"+val)
        Selectbox(lbl="dropna", options=[True, False], key="pivotTable_dropna")
        Selectbox(lbl="margins", options=[
                  False, True], key="pivotTable_margins")
        Selectbox(lbl="observed", options=[
                  False, True], key="pivotTable_observed")
        aggfunc = {}
        if len(values) > 0:
            for val in values:
                aggfunc[val] = st.session_state["pivotTable_aggfunc_"+val]
        index = st.session_state['pivotTable_index']
        columns = validate_col_value(st.session_state['pivotTable_columns'])
        dropna = st.session_state['pivotTable_dropna']
        margins = st.session_state['pivotTable_margins']
        observed = st.session_state['pivotTable_observed']

        try:
            df = pivot_table(data=data, index=index, columns=columns, dropna=dropna,
                             values=values, aggfunc=aggfunc, margins=margins, observed=observed)
            st.dataframe(df)
        except ValueError as e:
            st.write("No key passed.")
        except:
            st.write("Error updating pivot_table")

    if expander:
        with st.expander("pivot_table"):
            return index()
    return index()


def CrossTab(expander=True):
    cols = st.session_state['columns']
    data = st.session_state['df']

    def index():
        aggfuncOpt = list(pivotTable_aggfunc.keys())
        Selectbox(lbl="index", options=cols,
                  key="crossTab_index")
        Selectbox(lbl="columns", options=cols,
                  key="crossTab_columns")
        Selectbox(lbl="dropna", options=[True, False], key="crossTab_dropna")
        Selectbox(lbl="margins", options=[
                  False, True], key="crossTab_margins")
        Selectbox(lbl="normalize", options=[
                  False, True, 'all', 'index', 'columns'], key="crossTab_normalize")

        index = array(data[st.session_state['crossTab_index']]).flatten()
        columns = array(data[st.session_state['crossTab_columns']]).flatten()
        dropna = st.session_state['crossTab_dropna']
        margins = st.session_state['crossTab_margins']
        normalize = st.session_state['crossTab_normalize']
        try:
            df = crosstab(index=index, columns=columns,
                          dropna=dropna, normalize=normalize)
            st.dataframe(df)
        except:
            st.write("Error updating pivot_table")

    if expander:
        with st.expander("crosstab"):
            return index()
    return index()


def Cut(expander=True):
    cols = st.session_state['columns']
    data = st.session_state['df']
    cols_none = col_with_none()

    def index():
        Selectbox(lbl="x", options=cols, key="cut_x")
        x = array(data[st.session_state['cut_x']]).flatten()
        df = cut(x, 5)
        st.write(df)
    if expander:
        with st.expander("cut"):
            return index()
    return index()


def data_manipulation(expander=True):
    st.subheader("Data manipulation")
    Melt(expander)
    Pivot(expander)
    PivotTable(expander)
    CrossTab(expander)
    Cut(expander)
