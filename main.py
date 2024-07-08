import streamlit as st
from one import home
from results import res
from contact import contact

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Results", "Contact"])
    st.query_params["page"]=page
    if page == "Home":
        home()
    elif page == "Results":
        res()
    elif page == "Contact":
        contact()

if __name__ == "__main__":
    main()
