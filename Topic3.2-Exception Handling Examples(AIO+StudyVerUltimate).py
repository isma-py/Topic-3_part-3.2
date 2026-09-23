import streamlit as st
import streamlit.components.v1 as components
import sys
import io
import urllib.parse

# Page Configuration
st.set_page_config(
    page_title="Topic 3.2 Exception Handling", 
    layout="wide"
)

# Cisco Networking Academy Style Light Theme
st.markdown("""
    <style>
    /* Global Page Background & Text - Light Theme */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F8FAFC !important;
        color: #121820 !important;
    }
    
    /* Header Banner */
    [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
    }

    /* Headings - Cisco Dark Charcoal */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #121820 !important;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        font-weight: 700;
    }

    /* Paragraphs & Labels */
    p, label, span, div, .stMarkdown {
        color: #334155 !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    section[data-testid="stSidebar"] * {
        color: #121820 !important;
    }
    
    /* Frame Cards / Containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    /* Inputs & Text Areas */
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #121820 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-family: 'Fira Code', 'Courier New', monospace !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6CC24A !important;
        box-shadow: 0 0 0 2px rgba(108, 194, 74, 0.2) !important;
    }

    /* Code & Expander Styling */
    .stExpander {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }

    /* Cisco Signature Green Buttons */
    .stButton > button, .stLinkButton > a {
        background-color: #6CC24A !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        text-align: center !important;
        text-decoration: none !important;
        display: block !important;
    }
    .stButton > button:hover, .stLinkButton > a:hover {
        background-color: #58A63B !important;
        color: #FFFFFF !important;
    }

    /* Footer Branding */
    .footer-text {
        text-align: center;
        color: #64748B !important;
        font-size: 0.85rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #E2E8F0;
    }

    /* Responsive Mobile Layout */
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

# =========================================================
# Sidebar Navigation & Collapsible Music Section
# =========================================================
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

# Collapsible Music Section
with st.sidebar.expander("Music Section", expanded=True):
    music_mode = st.radio(
        "Select Source:",
        ["Live Station", "Search Music / Artist", "Spotify Player", "Custom YouTube URL"],
        key="music_mode_radio"
    )

    if music_mode == "Live Station":
        st.caption("Live Stream Radio")
        st.video("https://www.youtube.com/live/QmAbRBjcbY4")

    elif music_mode == "Search Music / Artist":
        search_query = st.text_input("Search Song or Artist:", "reidenshi")
        if search_query:
            encoded_query = urllib.parse.quote(search_query)
            yt_search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            ytm_search_url = f"https://music.youtube.com/search?q={encoded_query}"
            
            st.markdown(f"**Search Results for '{search_query}':**")
            st.link_button("Open on YouTube", yt_search_url)
            st.link_button("Open on YouTube Music", ytm_search_url)

    elif music_mode == "Spotify Player":
        spotify_url = st.text_input(
            "Paste Spotify Track/Playlist Link:", 
            "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT"
        )
        if spotify_url:
            embed_spotify = spotify_url.replace("open.spotify.com/", "open.spotify.com/embed/")
            components.iframe(embed_spotify, height=152)

    elif music_mode == "Custom YouTube URL":
        target_music = st.text_input("Paste YouTube Link:", "https://www.youtube.com/live/QmAbRBjcbY4")
        if target_music:
            st.video(target_music)

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