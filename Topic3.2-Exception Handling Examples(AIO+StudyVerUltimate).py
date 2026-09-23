import streamlit as st
import sys
import io

# Page Configuration
st.set_page_config(
    page_title="Topic 3.2 Exception Handling", 
    page_icon="🐍", 
    layout="wide"  # Wide layout gives full space for two side-by-side columns
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

# Helper function to execute custom user code inside a container
def execute_and_render(user_code, output_container):
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        with output_container:
            # Provide st to the custom execution scope
            exec_globals = {"st": st}
            exec(user_code, exec_globals)
            output = buffer.getvalue()
            if output:
                st.text_area("Console Output:", output, height=100)
    except Exception as e:
        output_container.error(f"Execution Error: {e}")
    finally:
        sys.stdout = sys.__stdout__


# =========================================================
# Demo 1: Basic Try-Except
# =========================================================
if demo_choice == "1. Basic Try-Except":
    st.title("Try Except Example")
    
    col_left, col_right = st.columns(2)
    
    # --- LEFT COLUMN: LIVE ORIGINAL APP ---
    with col_left:
        st.subheader("1. Original Live App")
        num = st.text_input("Enter a number", key="d1_num")
        if st.button("Check", key="d1_btn"):
            try:
                st.success(int(num))
            except:
                st.error("Invalid Input")

    # --- RIGHT COLUMN: PRACTICE SANDBOX ---
    with col_right:
        st.subheader("2. Practice Sandbox")
        ref_code_1 = """import streamlit as st

st.title("Try Except Example")
num = st.text_input("Enter a number")

if st.button("Check"):
    try:
        st.success(int(num))
    except:
        st.error("Invalid Input")"""

        user_code_1 = st.text_area(
            "Type your Python / Streamlit code here:",
            value=ref_code_1,
            height=200,
            key="d1_sandbox"
        )
        
        # Save execution state to keep output visible across button clicks
        if "d1_has_run" not in st.session_state:
            st.session_state.d1_has_run = False

        if st.button("▶ Run My Code", key="d1_run"):
            st.session_state.d1_has_run = True

        st.markdown("**Output of your code:**")
        output_box = st.container()
        if st.session_state.d1_has_run:
            execute_and_render(user_code_1, output_box)

        st.markdown("---")
        with st.expander("📖 View Reference Code", expanded=False):
            st.code(ref_code_1, language="python")


# =========================================================
# Demo 2: Age Checker (Else Clause)
# =========================================================
elif demo_choice == "2. Age Checker (Else Clause)":
    st.title("Age Checker")
    
    col_left, col_right = st.columns(2)
    
    # --- LEFT COLUMN: LIVE ORIGINAL APP ---
    with col_left:
        st.subheader("1. Original Live App")
        age = st.text_input("Enter your age", key="d2_age")
        if st.button("Check", key="d2_btn"):
            try:
                age = int(age)
            except:
                st.error("Invalid age")
            else:
                st.success("Age accepted")

    # --- RIGHT COLUMN: PRACTICE SANDBOX ---
    with col_right:
        st.subheader("2. Practice Sandbox")
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

        user_code_2 = st.text_area(
            "Type your Python / Streamlit code here:",
            value=ref_code_2,
            height=220,
            key="d2_sandbox"
        )
        
        if "d2_has_run" not in st.session_state:
            st.session_state.d2_has_run = False

        if st.button("▶ Run My Code", key="d2_run"):
            st.session_state.d2_has_run = True

        st.markdown("**Output of your code:**")
        output_box = st.container()
        if st.session_state.d2_has_run:
            execute_and_render(user_code_2, output_box)

        st.markdown("---")
        with st.expander("📖 View Reference Code", expanded=False):
            st.code(ref_code_2, language="python")


# =========================================================
# Demo 3: Name Submission (Finally Clause)
# =========================================================
elif demo_choice == "3. Name Submission (Finally Clause)":
    st.title("Try Except Else Finally")
    
    col_left, col_right = st.columns(2)
    
    # --- LEFT COLUMN: LIVE ORIGINAL APP ---
    with col_left:
        st.subheader("1. Original Live App")
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

    # --- RIGHT COLUMN: PRACTICE SANDBOX ---
    with col_right:
        st.subheader("2. Practice Sandbox")
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

        user_code_3 = st.text_area(
            "Type your Python / Streamlit code here:",
            value=ref_code_3,
            height=260,
            key="d3_sandbox"
        )
        
        if "d3_has_run" not in st.session_state:
            st.session_state.d3_has_run = False

        if st.button("▶ Run My Code", key="d3_run"):
            st.session_state.d3_has_run = True

        st.markdown("**Output of your code:**")
        output_box = st.container()
        if st.session_state.d3_has_run:
            execute_and_render(user_code_3, output_box)

        st.markdown("---")
        with st.expander("📖 View Reference Code", expanded=False):
            st.code(ref_code_3, language="python")


# =========================================================
# Demo 4: Email Validation (Custom Exception)
# =========================================================
elif demo_choice == "4. Email Validation (Custom Exception)":
    st.title("Email Validation")
    
    col_left, col_right = st.columns(2)
    
    # --- LEFT COLUMN: LIVE ORIGINAL APP ---
    with col_left:
        st.subheader("1. Original Live App")
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

    # --- RIGHT COLUMN: PRACTICE SANDBOX ---
    with col_right:
        st.subheader("2. Practice Sandbox")
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

        user_code_4 = st.text_area(
            "Type your Python / Streamlit code here:",
            value=ref_code_4,
            height=280,
            key="d4_sandbox"
        )
        
        if "d4_has_run" not in st.session_state:
            st.session_state.d4_has_run = False

        if st.button("▶ Run My Code", key="d4_run"):
            st.session_state.d4_has_run = True

        st.markdown("**Output of your code:**")
        output_box = st.container()
        if st.session_state.d4_has_run:
            execute_and_render(user_code_4, output_box)

        st.markdown("---")
        with st.expander("📖 View Reference Code", expanded=False):
            st.code(ref_code_4, language="python")