import streamlit as st
import sys
import io

# Page Configuration
st.set_page_config(
    page_title="Topic 3.2 Exception Handling", 
    page_icon="⚡", 
    layout="wide"
)

# Custom Cisco-Inspired CSS Theme & Mobile Responsive Rules
st.markdown("""
    <style>
    /* Main Background & Fonts */
    .main {
        background-color: #F8FAFC;
    }
    
    /* Header & Subheader Colors */
    h1 {
        color: #002C6C !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
    }
    h2, h3 {
        color: #002C6C !important;
    }
    
    /* Custom Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #002C6C !important;
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* Custom Button Styling (Cisco Blue) */
    .stButton > button {
        background-color: #00BCEB !important;
        color: #FFFFFF !important;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #009DC8 !important;
        box-shadow: 0 4px 12px rgba(0, 188, 235, 0.3);
    }

    /* Mobile Responsive Adjustments */
    @media (max-width: 768px) {
        .row-widget.stColumns {
            flex-direction: column !important;
        }
        div[data-testid="column"] {
            width: 100% !important;
            margin-bottom: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("⚡ Cisco Python Lab")
st.sidebar.subheader("Topic 3.2 Exception Handling")
demo_choice = st.sidebar.radio(
    "Select Module:",
    [
        "1. Basic Try-Except",
        "2. Age Checker (Else Clause)",
        "3. Name Submission (Finally Clause)",
        "4. Email Validation (Custom Exception)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("DFK50083 Python Programming\nTopic 3.0: GUI Design & Exception Handling")

# Helper function to execute custom user code inside a container
def execute_and_render(user_code, output_container):
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        with output_container:
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
    st.markdown(
        "**Explanation:** The `try` block tests a block of code for runtime errors, "
        "while the `except` block catches and handles errors (such as entering invalid text "
        "when converting to an integer) to prevent the program from crashing."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    # --- LEFT PANEL: THE CODE ---
    with col_left:
        with st.container(border=True):
            st.subheader("The Code")
            num = st.text_input("Enter a number", key="d1_num")
            if st.button("Check", key="d1_btn"):
                try:
                    st.success(int(num))
                except:
                    st.error("Invalid Input")

            st.markdown("---")
            ref_code_1 = """import streamlit as st

st.title("Try Except Example")
num = st.text_input("Enter a number")

if st.button("Check"):
    try:
        st.success(int(num))
    except:
        st.error("Invalid Input")"""

            with st.expander("📖 View Reference Code", expanded=False):
                st.code(ref_code_1, language="python")

    # --- RIGHT PANEL: TEST YOUR SELF ---
    with col_right:
        with st.container(border=True):
            st.subheader("Test Your Self")
            user_code_1 = st.text_area(
                "Type your Python / Streamlit code here:",
                value=ref_code_1,
                height=180,
                key="d1_sandbox"
            )
            
            if "d1_has_run" not in st.session_state:
                st.session_state.d1_has_run = False

            if st.button("▶ Run My Code", key="d1_run"):
                st.session_state.d1_has_run = True

            st.markdown("**Output of your code:**")
            
            with st.container(border=True):
                if st.session_state.d1_has_run:
                    execute_and_render(user_code_1, st.container())
                else:
                    st.info("Click '▶ Run My Code' to view output inside this frame.")


# =========================================================
# Demo 2: Age Checker (Else Clause)
# =========================================================
elif demo_choice == "2. Age Checker (Else Clause)":
    st.title("Age Checker")
    st.markdown(
        "**Explanation:** The `else` clause executes **only if no errors occurred** inside "
        "the `try` block. In this example, if integer conversion succeeds, the `else` block "
        "triggers the success message."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    # --- LEFT PANEL: THE CODE ---
    with col_left:
        with st.container(border=True):
            st.subheader("The Code")
            age = st.text_input("Enter your age", key="d2_age")
            if st.button("Check", key="d2_btn"):
                try:
                    age = int(age)
                except:
                    st.error("Invalid age")
                else:
                    st.success("Age accepted")

            st.markdown("---")
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

            with st.expander("📖 View Reference Code", expanded=False):
                st.code(ref_code_2, language="python")

    # --- RIGHT PANEL: TEST YOUR SELF ---
    with col_right:
        with st.container(border=True):
            st.subheader("Test Your Self")
            user_code_2 = st.text_area(
                "Type your Python / Streamlit code here:",
                value=ref_code_2,
                height=200,
                key="d2_sandbox"
            )
            
            if "d2_has_run" not in st.session_state:
                st.session_state.d2_has_run = False

            if st.button("▶ Run My Code", key="d2_run"):
                st.session_state.d2_has_run = True

            st.markdown("**Output of your code:**")
            
            with st.container(border=True):
                if st.session_state.d2_has_run:
                    execute_and_render(user_code_2, st.container())
                else:
                    st.info("Click '▶ Run My Code' to view output inside this frame.")


# =========================================================
# Demo 3: Name Submission (Finally Clause)
# =========================================================
elif demo_choice == "3. Name Submission (Finally Clause)":
    st.title("Try Except Else Finally")
    st.markdown(
        "**Explanation:** The `finally` clause **always runs** regardless of whether an exception "
        "was raised or caught. It is commonly used for cleanup actions, such as closing files "
        "or logging 'Program End'."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    # --- LEFT PANEL: THE CODE ---
    with col_left:
        with st.container(border=True):
            st.subheader("The Code")
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

            with st.expander("📖 View Reference Code", expanded=False):
                st.code(ref_code_3, language="python")

    # --- RIGHT PANEL: TEST YOUR SELF ---
    with col_right:
        with st.container(border=True):
            st.subheader("Test Your Self")
            user_code_3 = st.text_area(
                "Type your Python / Streamlit code here:",
                value=ref_code_3,
                height=240,
                key="d3_sandbox"
            )
            
            if "d3_has_run" not in st.session_state:
                st.session_state.d3_has_run = False

            if st.button("▶ Run My Code", key="d3_run"):
                st.session_state.d3_has_run = True

            st.markdown("**Output of your code:**")
            
            with st.container(border=True):
                if st.session_state.d3_has_run:
                    execute_and_render(user_code_3, st.container())
                else:
                    st.info("Click '▶ Run My Code' to view output inside this frame.")


# =========================================================
# Demo 4: Email Validation (Custom Exception)
# =========================================================
elif demo_choice == "4. Email Validation (Custom Exception)":
    st.title("Email Validation")
    st.markdown(
        "**Explanation:** Python allows raising custom exceptions manually using `raise ValueError('message')`. "
        "The `except ValueError as e` block captures the exact error message string and displays it using Streamlit."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    # --- LEFT PANEL: THE CODE ---
    with col_left:
        with st.container(border=True):
            st.subheader("The Code")
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

            with st.expander("📖 View Reference Code", expanded=False):
                st.code(ref_code_4, language="python")

    # --- RIGHT PANEL: TEST YOUR SELF ---
    with col_right:
        with st.container(border=True):
            st.subheader("Test Your Self")
            user_code_4 = st.text_area(
                "Type your Python / Streamlit code here:",
                value=ref_code_4,
                height=260,
                key="d4_sandbox"
            )
            
            if "d4_has_run" not in st.session_state:
                st.session_state.d4_has_run = False

            if st.button("▶ Run My Code", key="d4_run"):
                st.session_state.d4_has_run = True

            st.markdown("**Output of your code:**")
            
            with st.container(border=True):
                if st.session_state.d4_has_run:
                    execute_and_render(user_code_4, st.container())
                else:
                    st.info("Click '▶ Run My Code' to view output inside this frame.")