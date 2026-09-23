import streamlit as st
import sys
import io

# Page Configuration
st.set_page_config(
    page_title="Topic 3.2 Exception Handling", 
    layout="wide"
)

# Responsive & Mode-Independent CSS Theme Fix
st.markdown("""
    <style>
    /* Force consistent dark slate background across entire page in all modes */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }
    
    /* Ensure Header banner matches dark background */
    [data-testid="stHeader"] {
        background-color: #0F172A !important;
    }

    /* All Header Texts forced bright white */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #F8FAFC !important;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        font-weight: 600;
    }

    /* Paragraphs, Labels, and Explanations */
    p, label, span, div, .stMarkdown {
        color: #E2E8F0 !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }
    section[data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }
    
    /* Framed Container Boxes */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #182232 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    /* Input Fields & Text Area Code Box */
    .stTextInput input, .stTextArea textarea {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #475569 !important;
        border-radius: 6px !important;
        font-family: 'Fira Code', 'Courier New', monospace !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #52796F !important;
        box-shadow: 0 0 0 1px #52796F !important;
    }

    /* Expander / Reference Code Styling */
    .stExpander {
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
    }

    /* Button Styling */
    .stButton > button {
        background-color: #52796F !important;
        color: #FFFFFF !important;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 0.4rem 1rem;
        transition: background-color 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #354F52 !important;
        color: #FFFFFF !important;
    }

    /* Footer Branding */
    .footer-text {
        text-align: center;
        color: #94A3B8 !important;
        font-size: 0.85rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #334155;
    }

    /* Mobile Responsive Rules */
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
st.sidebar.title("Python Lab Environment")
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
st.sidebar.markdown("**Created by IsmaPY**")

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

            with st.expander("View Reference Code", expanded=False):
                st.code(ref_code_1, language="python")

    # --- RIGHT PANEL: TEST YOUR SELF ---
    with col_right:
        with st.container(border=True):
            st.subheader("Test Your Self")
            user_code_1 = st.text_area(
                "Your Code",
                value="",
                height=180,
                key="d1_sandbox"
            )
            
            if "d1_has_run" not in st.session_state:
                st.session_state.d1_has_run = False

            if st.button("Run My Code", key="d1_run"):
                st.session_state.d1_has_run = True

            st.markdown("**Output of your code:**")
            
            with st.container(border=True):
                if st.session_state.d1_has_run:
                    execute_and_render(user_code_1, st.container())
                else:
                    st.info("Click 'Run My Code' to view output inside this frame.")


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

            with st.expander("View Reference Code", expanded=False):
                st.code(ref_code_2, language="python")

    # --- RIGHT PANEL: TEST YOUR SELF ---
    with col_right:
        with st.container(border=True):
            st.subheader("Test Your Self")
            user_code_2 = st.text_area(
                "Your Code",
                value="",
                height=200,
                key="d2_sandbox"
            )
            
            if "d2_has_run" not in st.session_state:
                st.session_state.d2_has_run = False

            if st.button("Run My Code", key="d2_run"):
                st.session_state.d2_has_run = True

            st.markdown("**Output of your code:**")
            
            with st.container(border=True):
                if st.session_state.d2_has_run:
                    execute_and_render(user_code_2, st.container())
                else:
                    st.info("Click 'Run My Code' to view output inside this frame.")


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

            with st.expander("View Reference Code", expanded=False):
                st.code(ref_code_3, language="python")

    # --- RIGHT PANEL: TEST YOUR SELF ---
    with col_right:
        with st.container(border=True):
            st.subheader("Test Your Self")
            user_code_3 = st.text_area(
                "Your Code",
                value="",
                height=240,
                key="d3_sandbox"
            )
            
            if "d3_has_run" not in st.session_state:
                st.session_state.d3_has_run = False

            if st.button("Run My Code", key="d3_run"):
                st.session_state.d3_has_run = True

            st.markdown("**Output of your code:**")
            
            with st.container(border=True):
                if st.session_state.d3_has_run:
                    execute_and_render(user_code_3, st.container())
                else:
                    st.info("Click 'Run My Code' to view output inside this frame.")


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

            with st.expander("View Reference Code", expanded=False):
                st.code(ref_code_4, language="python")

    # --- RIGHT PANEL: TEST YOUR SELF ---
    with col_right:
        with st.container(border=True):
            st.subheader("Test Your Self")
            user_code_4 = st.text_area(
                "Your Code",
                value="",
                height=260,
                key="d4_sandbox"
            )
            
            if "d4_has_run" not in st.session_state:
                st.session_state.d4_has_run = False

            if st.button("Run My Code", key="d4_run"):
                st.session_state.d4_has_run = True

            st.markdown("**Output of your code:**")
            
            with st.container(border=True):
                if st.session_state.d4_has_run:
                    execute_and_render(user_code_4, st.container())
                else:
                    st.info("Click 'Run My Code' to view output inside this frame.")

# Footer Signature
st.markdown('<div class="footer-text">Created by IsmaPY</div>', unsafe_allow_html=True)