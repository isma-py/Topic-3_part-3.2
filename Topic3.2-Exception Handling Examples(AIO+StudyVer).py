import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Topic 3.2 Exception Handling", 
    page_icon="🐍", 
    layout="centered"
)

# Sidebar Navigation
st.sidebar.title("Topic 3.2 Navigation")
demo_choice = st.sidebar.radio(
    "Select an Exception Handling Demo:",
    [
        "1. Basic Try-Except",
        "2. Age Checker (Else Clause)",
        "3. Name Submission (Finally Clause)",
        "4. Email Validation (Custom Exception)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("DFK50083 Python Programming\nTopic 3.0: GUI Design & Exception Handling")

# =========================================================
# Demo 1: Basic Try-Except
# =========================================================
if demo_choice == "1. Basic Try-Except":
    st.title("Try Except Example")
    
    num = st.text_input("Enter a number")

    if st.button("Check"):
        try:
            st.success(int(num))
        except:
            st.error("Invalid Input")

    # Code Viewer for Study
    st.markdown("---")
    with st.expander("📖 View Python Code for this page"):
        st.code("""
import streamlit as st

st.title("Try Except Example")

num = st.text_input("Enter a number")

if st.button("Check"):
    try:
        st.success(int(num))
    except:
        st.error("Invalid Input")
        """, language="python")


# =========================================================
# Demo 2: Age Checker (Else Clause)
# =========================================================
elif demo_choice == "2. Age Checker (Else Clause)":
    st.title("Age Checker")
    
    age = st.text_input("Enter your age")

    if st.button("Check"):
        try:
            age = int(age)
        except:
            st.error("Invalid age")
        else:
            st.success("Age accepted")

    # Code Viewer for Study
    st.markdown("---")
    with st.expander("📖 View Python Code for this page"):
        st.code("""
import streamlit as st

st.title("Age Checker")

age = st.text_input("Enter your age")

if st.button("Check"):
    try:
        age = int(age)
    except:
        st.error("Invalid age")
    else:
        st.success("Age accepted")
        """, language="python")


# =========================================================
# Demo 3: Name Submission (Finally Clause)
# =========================================================
elif demo_choice == "3. Name Submission (Finally Clause)":
    st.title("Try Except Else Finally")
    
    name = st.text_input("Enter your name")

    if st.button("Submit"):
        try:
            if name == "":
                raise ValueError
        except:
            st.error("Please enter your name")
        else:
            st.success("Welcome " + name)
        finally:
            st.write("Program End")

    # Code Viewer for Study
    st.markdown("---")
    with st.expander("📖 View Python Code for this page"):
        st.code("""
import streamlit as st

st.title("Try Except Else Finally")

name = st.text_input("Enter your name")

if st.button("Submit"):
    try:
        if name == "":
            raise ValueError
    except:
        st.error("Please enter your name")
    else:
        st.success("Welcome " + name)
    finally:
        st.write("Program End")
        """, language="python")


# =========================================================
# Demo 4: Email Validation (Custom Exception)
# =========================================================
elif demo_choice == "4. Email Validation (Custom Exception)":
    st.title("Email Validation")
    
    email = st.text_input("Enter Email")

    if st.button("Submit"):
        try:
            if email == "":
                raise ValueError("Please Insert Email")
            elif "@" not in email:
                raise ValueError("Invalid Email")
        except ValueError as e:
            st.error(e)
        else:
            st.success("Email Accepted")
        finally:
            st.info("Done")

    # Code Viewer for Study
    st.markdown("---")
    with st.expander("📖 View Python Code for this page"):
        st.code("""
import streamlit as st

st.title("Email Validation")

email = st.text_input("Enter Email")

if st.button("Submit"):
    try:
        if email == "":
            raise ValueError("Please Insert Email")
        elif "@" not in email:
            raise ValueError("Invalid Email")
    except ValueError as e:
        st.error(e)
    else:
        st.success("Email Accepted")
    finally:
        st.info("Done")
        """, language="python")