import streamlit as st
import sys
import io

# Page Configuration
st.set_page_config(
    page_title="Topic 3.2 Exception Handling", 
    page_icon="🐍", 
    layout="wide"
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

# Helper function to execute user code and capture output
def run_user_code(user_code):
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        # Create a local scope for execution
        exec_globals = {"st": st}
        exec(user_code, exec_globals)
        output = buffer.getvalue()
        if output:
            st.text_area("Console Output:", output, height=120)
    except Exception as e:
        st.error(f"Execution Error: {e}")
    finally:
        sys.stdout = sys.__stdout__


# =========================================================
# Demo 1: Basic Try-Except
# =========================================================
if demo_choice == "1. Basic Try-Except":
    st.title("Try Except Example")
    
    # 1. Live Interactive App
    st.subheader("1. Live Demo")
    num = st.text_input("Enter a number", key="d1_num")
    if st.button("Check", key="d1_btn"):
        try:
            st.success(int(num))
        except:
            st.error("Invalid Input")

    st.markdown("---")

    # 2. Reference Code Box
    with st.expander("📖 2. Reference Code (Click to Expand)", expanded=False):
        ref_code_1 = """import streamlit as st

st.title("Try Except Example")
num = st.text_input("Enter a number")

if st.button("Check"):
    try:
        st.success(int(num))
    except:
        st.error("Invalid Input")"""
        st.code(ref_code_1, language="python")

    st.markdown("---")

    # 3. Practice Sandbox
    st.subheader("3. Practice Sandbox (Type & Test Your Code)")
    user_code_1 = st.text_area(
        "Type your Python / Streamlit code here:",
        value=ref_code_1,
        height=200,
        key="d1_sandbox"
    )
    if st.button("▶ Run My Code", key="d1_run"):
        st.markdown("**Output of your code:**")
        run_user_code(user_code_1)


# =========================================================
# Demo 2: Age Checker (Else Clause)
# =========================================================
elif demo_choice == "2. Age Checker (Else Clause)":
    st.title("Age Checker")
    
    # 1. Live Interactive App
    st.subheader("1. Live Demo")
    age = st.text_input("Enter your age", key="d2_age")
    if st.button("Check", key="d2_btn"):
        try:
            age = int(age)
        except:
            st.error("Invalid age")
        else:
            st.success("Age accepted")

    st.markdown("---")

    # 2. Reference Code Box
    with st.expander("📖 2. Reference Code (Click to Expand)", expanded=False):
        ref_code_2 = """import streamlit as st

st.title("Age Checker")
age = st.text_input("Enter your age")

if st.button("Check"):
    try:
        age = int(age)
    except:
        st.error("Invalid age")
    else:
        st.success("Age accepted")"""
        st.code(ref_code_2, language="python")

    st.markdown("---")

    # 3. Practice Sandbox
    st.subheader("3. Practice Sandbox (Type & Test Your Code)")
    user_code_2 = st.text_area(
        "Type your Python / Streamlit code here:",
        value=ref_code_2,
        height=220,
        key="d2_sandbox"
    )
    if st.button("▶ Run My Code", key="d2_run"):
        st.markdown("**Output of your code:**")
        run_user_code(user_code_2)


# =========================================================
# Demo 3: Name Submission (Finally Clause)
# =========================================================
elif demo_choice == "3. Name Submission (Finally Clause)":
    st.title("Try Except Else Finally")
    
    # 1. Live Interactive App
    st.subheader("1. Live Demo")
    name = st.text_input("Enter your name", key="d3_name")
    if st.button("Submit", key="d3_btn"):
        try:
            if name == "":
                raise ValueError
        except:
            st.error("Please enter your name")
        else:
            st.success("Welcome " + name)
        finally:
            st.write("Program End")

    st.markdown("---")

    # 2. Reference Code Box
    with st.expander("📖 2. Reference Code (Click to Expand)", expanded=False):
        ref_code_3 = """import streamlit as st

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
        st.write("Program End")"""
        st.code(ref_code_3, language="python")

    st.markdown("---")

    # 3. Practice Sandbox
    st.subheader("3. Practice Sandbox (Type & Test Your Code)")
    user_code_3 = st.text_area(
        "Type your Python / Streamlit code here:",
        value=ref_code_3,
        height=260,
        key="d3_sandbox"
    )
    if st.button("▶ Run My Code", key="d3_run"):
        st.markdown("**Output of your code:**")
        run_user_code(user_code_3)


# =========================================================
# Demo 4: Email Validation (Custom Exception)
# =========================================================
elif demo_choice == "4. Email Validation (Custom Exception)":
    st.title("Email Validation")
    
    # 1. Live Interactive App
    st.subheader("1. Live Demo")
    email = st.text_input("Enter Email", key="d4_email")
    if st.button("Submit", key="d4_btn"):
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

    st.markdown("---")

    # 2. Reference Code Box
    with st.expander("📖 2. Reference Code (Click to Expand)", expanded=False):
        ref_code_4 = """import streamlit as st

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
        st.info("Done")"""
        st.code(ref_code_4, language="python")

    st.markdown("---")

    # 3. Practice Sandbox
    st.subheader("3. Practice Sandbox (Type & Test Your Code)")
    user_code_4 = st.text_area(
        "Type your Python / Streamlit code here:",
        value=ref_code_4,
        height=280,
        key="d4_sandbox"
    )
    if st.button("▶ Run My Code", key="d4_run"):
        st.markdown("**Output of your code:**")
        run_user_code(user_code_4)