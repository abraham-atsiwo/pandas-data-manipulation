import streamlit as st

def key_generator(lbl, key=None):
    if key is None:
        key = lbl.replace(" ", "_").lower().strip()
    else:
        key = key
    return key

def Selectbox(lbl, options=[], key=None):
    key = key_generator(lbl, key)
    st.selectbox(label=lbl, options=options, key=key)

def Multiselect(lbl, options=[], default=[], key=None):
    key = key_generator(lbl, key)
    st.multiselect(lbl, options, key=key, default=default)


def File_uploader(lbl, key=None, type=None):
    key = key_generator(lbl, key)
    st.file_uploader(label=lbl, type=type, key=key)