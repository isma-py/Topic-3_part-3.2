import streamlit as st
import streamlit.components.v1 as components
import sys
import io
import urllib.parse
import requests
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Built-in Python 3.9+ library for timezones

# Target Timezone for Malaysia (GMT+8)
LOCAL_TZ = ZoneInfo("Asia/Kuala_Lumpur")

# Page Configuration
st.set_page_config(
    page_title="Topic 3.2 Exception Handling", 
    layout="wide"
)

# Discord Webhook Configurations
LOGIN_WEBHOOK_URL = "https://discord.com/api/webhooks/1552364753605886092/M_01xSCjvxShmz_coHn3ywRnRn6PTqf-LOxeVQq2kn7Wy-zHnndI_doa64x7_sAhjF1B"
BUG_WEBHOOK_URL = "https://discord.com/api/webhooks/1552366425706987552/2fmHmPjquJ9yPCa2Hgb6naZFB0gsE1UfPuiZlh1zO38EMsyQWQq1bcgWhol75jICe-v8"

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
    
    /* Disabled Button Style */
    .stButton > button:disabled {
        background-color: #CBD5E1 !important;
        color: #64748B !important;
        cursor: not-allowed !important;
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

# Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "show_light_mode_modal" not in st.session_state:
    st.session_state.show_light_mode_modal = False

if "last_login_time" not in st.session_state:
    st.session_state.last_login_time = None

if "last_bug_report_time" not in st.session_state:
    st.session_state.last_bug_report_time = None


@st.dialog("Important Notice")
def show_light_mode_dialog():
    st.write(
        "Please ensure your browser settings are adjusted properly for the best "
        "visual display and interface performance before proceeding."
    )
    st.warning(
        "**Progress Tracking Notice:** This webpage does **not** have a database to store "
        "your progress or code inputs. Please remember to log or record your progress "
        "manually if needed!"
    )
    if st.button("I Understand & Proceed"):
        st.session_state.show_light_mode_modal = False
        st.rerun()


def send_discord_log(user_name, camera_file_bytes):
    """Sends login timestamp (GMT+8), student username, and face capture image to Discord Webhook."""
    now = datetime.now(LOCAL_TZ)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%I:%M:%S %p")

    payload = {
        "embeds": [
            {
                "title": "Lab Access & Attendance Log",
                "color": 7127626,  # Cisco Green #6CC24A
                "fields": [
                    {"name": "Student Name", "value": f"**{user_name}**", "inline": True},
                    {"name": "Date", "value": date_str, "inline": True},
                    {"name": "Time (GMT+8)", "value": time_str, "inline": True},
                    {"name": "Topic", "value": "Topic 3.2 Exception Handling", "inline": False}
                ],
                "image": {"url": "attachment://face_capture.png"},
                "footer": {"text": "Python Lab Environment | Attendance Verification"}
            }
        ]
    }

    files = {
        "payload_json": (None, json.dumps(payload), "application/json"),
        "file": ("face_capture.png", camera_file_bytes, "image/png")
    }

    try:
        requests.post(LOGIN_WEBHOOK_URL, files=files, timeout=10)
    except Exception as e:
        st.error(f"Failed to log access: {e}")


def send_bug_report(user_name, bug_category, bug_description, bug_file_bytes=None):
    """Sends bug report along with student name, timestamp, and optional evidence photo to Discord Webhook."""
    now = datetime.now(LOCAL_TZ)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%I:%M:%S %p")

    embed = {
        "title": "Issue / Bug Report Submitted",
        "color": 15158332,  # Warning Red/Orange
        "fields": [
            {"name": "Reported By", "value": f"**{user_name}**", "inline": True},
            {"name": "Category", "value": bug_category, "inline": True},
            {"name": "Date & Time (GMT+8)", "value": f"{date_str} at {time_str}", "inline": False},
            {"name": "Issue Description", "value": bug_description, "inline": False}
        ],
        "footer": {"text": "Python Lab Environment | Bug Tracker"}
    }

    if bug_file_bytes:
        embed["image"] = {"url": "attachment://bug_evidence.png"}

    payload = {"embeds": [embed]}

    try:
        if bug_file_bytes:
            files = {
                "payload_json": (None, json.dumps(payload), "application/json"),
                "file": ("bug_evidence.png", bug_file_bytes, "image/png")
            }
            response = requests.post(BUG_WEBHOOK_URL, files=files, timeout=10)
        else:
            response = requests.post(BUG_WEBHOOK_URL, json=payload, timeout=5)

        return response.status_code in [200, 204]
    except Exception:
        return False


# =========================================================
# LOGIN GATEKEEPER SCREEN (NAME + MANDATORY FACE CAPTURE)
# =========================================================
if not st.session_state.authenticated:
    _, col_main, _ = st.columns([1, 2, 1])
    
    with col_main:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.title("Python Lab Access Gateway")
            st.markdown("Please enter your full name and take a face photo to verify attendance to log in")
            
            student_name = st.text_input("Full Name:", key="student_name_input", placeholder="e.g. John Doe")
            
            st.markdown("**Face Verification Capture:**")
            camera_photo = st.camera_input("Take a photo to proceed", key="login_camera_input")
            
            # Check if login is currently under a 3-minute cooldown
            now_login = datetime.now(LOCAL_TZ)
            login_on_cooldown = False
            login_remaining = 0
            if st.session_state.last_login_time is not None:
                elapsed = (now_login - st.session_state.last_login_time).total_seconds()
                if elapsed < 180:  # 3 minutes = 180 seconds
                    login_on_cooldown = True
                    login_remaining = int(180 - elapsed)

            if login_on_cooldown:
                st.warning(f"Submission locked. Please wait {login_remaining // 60}m {login_remaining % 60}s before logging in again.")

            if st.button("Enter Lab", disabled=login_on_cooldown):
                now = datetime.now(LOCAL_TZ)
                if student_name.strip() == "":
                    st.error("Please enter your name before proceeding.")
                elif camera_photo is None:
                    st.error("Face capture is required! Please click 'Take Photo' above.")
                else:
                    file_bytes = camera_photo.getvalue()
                    send_discord_log(student_name.strip(), file_bytes)
                    
                    st.session_state.last_login_time = now
                    st.session_state.authenticated = True
                    st.session_state.student_name = student_name.strip()
                    st.session_state.show_light_mode_modal = True  # Trigger modal upon login
                    st.rerun()

    st.stop()


# Trigger Reminder Dialog if user just logged in
if st.session_state.show_light_mode_modal:
    show_light_mode_dialog()


# =========================================================
# MAIN APP ENVIRONMENT (REACHABLE ONLY AFTER LOGIN)
# =========================================================

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


# Sidebar Navigation & Collapsible Sections
st.sidebar.title("Python Lab Environment")
st.sidebar.caption(f"Logged in as: **{st.session_state.get('student_name', 'Student')}**")
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

# 1. Collapsible Music Section
with st.sidebar.expander("Music Section", expanded=False):
    music_mode = st.radio(
        "Select Source:",
        ["Preset Track", "Search Music / Artist", "Spotify Player", "Custom YouTube URL"],
        key="music_mode_radio"
    )

    if music_mode == "Preset Track":
        preset_tracks = [
            {"title": "øneheart x reidenshi - snowfall", "id": "LlN8MPS7KQs"},
            {"title": "hozuki - time", "id": "kvprs8s-qI8"},
            {"title": "willix - blue_pool", "id": "3rUiU6VQsr4"},
            {"title": "øneheart, remind me, leadwave, dean korso - under the rising sun", "id": "IpXY-Txccts"},
            {"title": "since 1993 - a fever dream", "id": "umxwelP57cY"},
            {"title": ".diedlonely, envacity - losing", "id": "0ONE_X_1ufc"}
        ]

        music_selection = st.selectbox(
            "Choose Track:",
            options=range(len(preset_tracks)),
            format_func=lambda i: preset_tracks[i]["title"]
        )

        selected_id = preset_tracks[music_selection]["id"]
        playlist_ids = ",".join([track["id"] for track in preset_tracks[music_selection:]])

        player_html = f"""
        <div style="width: 100%;">
            <div id="player"></div>
            
            <div class="clean-volume-box">
                <div class="clean-volume-label">Volume</div>
                <input 
                    type="range" 
                    id="volumeSlider" 
                    min="0" 
                    max="1" 
                    step="0.01" 
                    value="0.8" 
                />
            </div>
        </div>

        <style>
          .clean-volume-box {{
            margin-top: 12px;
            padding: 0px;
          }}

          .clean-volume-label {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            font-size: 0.875rem;
            font-weight: 500;
            color: #334155;
            margin-bottom: 6px;
          }}

          input[type="range"]#volumeSlider {{
            -webkit-appearance: none;
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: linear-gradient(to right, #6CC24A var(--vol-fill, 80%), #E2E8F0 var(--vol-fill, 80%));
            outline: none;
            cursor: pointer;
          }}

          input[type="range"]#volumeSlider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #6CC24A;
            border: 2px solid #FFFFFF;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            transition: transform 0.1s ease;
          }}

          input[type="range"]#volumeSlider::-webkit-slider-thumb:hover {{
            transform: scale(1.15);
          }}
        </style>

        <script>
            var tag = document.createElement('script');
            tag.src = "https://www.youtube.com/iframe_api";
            var firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

            var player;
            var storedVolume = localStorage.getItem('globalPlayerVolume');
            var initialVol = storedVolume !== null ? parseFloat(storedVolume) : 0.8;

            function onYouTubeIframeAPIReady() {{
                player = new YT.Player('player', {{
                    height: '170',
                    width: '100%',
                    videoId: '{selected_id}',
                    playerVars: {{
                        'autoplay': 1,
                        'playlist': '{playlist_ids}',
                        'playsinline': 1
                    }},
                    events: {{
                        'onReady': onPlayerReady,
                        'onStateChange': onPlayerStateChange
                    }}
                }});
            }}

            function applyVolume(val) {{
                if (player && player.setVolume) {{
                    player.setVolume(val * 100);
                }}
                const slider = document.getElementById('volumeSlider');
                if (slider) {{
                    slider.value = val;
                    let perc = Math.round(val * 100);
                    slider.style.setProperty('--vol-fill', perc + '%');
                }}
            }}

            function onPlayerReady(event) {{
                applyVolume(initialVol);
                event.target.playVideo();
                
                const slider = document.getElementById('volumeSlider');
                slider.addEventListener('input', function() {{
                    let val = this.value;
                    localStorage.setItem('globalPlayerVolume', val);
                    applyVolume(val);
                }});
            }}

            function onPlayerStateChange(event) {{
                var currentVol = localStorage.getItem('globalPlayerVolume');
                if (currentVol !== null) {{
                    applyVolume(parseFloat(currentVol));
                }}
            }}
        </script>
        """
        components.html(player_html, height=260)

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
        target_music = st.text_input("Paste YouTube Link:", "https://www.youtube.com/watch?v=kvprs8s-qI8")
        if target_music:
            st.video(target_music)

# 2. Collapsible Bug / Issue Reporting Section with Evidence Upload & Cooldown
with st.sidebar.expander("Report Issues / Bug", expanded=False):
    st.markdown("Found an issue? Submit details below to notify Isma.")
    
    bug_category = st.selectbox(
        "Issue Type:",
        ["General Bug", "Audio / Player Issue", "Code Execution Error", "Interface Formatting", "Other"]
    )
    
    bug_desc = st.text_area("Describe the issue:", placeholder="Explain what happened...", height=100)
    
    uploaded_evidence = st.file_uploader(
        "Attach Evidence / Screenshot (Optional):", 
        type=["png", "jpg", "jpeg"],
        key="bug_evidence_uploader"
    )
    
    # Check if bug report is currently under a 3-minute cooldown
    now_bug = datetime.now(LOCAL_TZ)
    bug_on_cooldown = False
    bug_remaining = 0
    if st.session_state.last_bug_report_time is not None:
        elapsed_bug = (now_bug - st.session_state.last_bug_report_time).total_seconds()
        if elapsed_bug < 180:  # 3 minutes = 180 seconds
            bug_on_cooldown = True
            bug_remaining = int(180 - elapsed_bug)

    if bug_on_cooldown:
        st.warning(f"Report locked. Please wait {bug_remaining // 60}m {bug_remaining % 60}s before submitting another report.")

    if st.button("Submit Report", disabled=bug_on_cooldown):
        now = datetime.now(LOCAL_TZ)
        if bug_desc.strip() == "":
            st.error("Please describe the issue before submitting.")
        else:
            current_user = st.session_state.get('student_name', 'Anonymous Student')
            file_bytes = uploaded_evidence.getvalue() if uploaded_evidence is not None else None
            
            success = send_bug_report(current_user, bug_category, bug_desc.strip(), file_bytes)
            
            if success:
                st.session_state.last_bug_report_time = now
                st.success("Report submitted successfully!")
                st.rerun()
            else:
                st.error("Failed to send report. Please try again.")

st.sidebar.markdown("---")
st.sidebar.caption("DFK50083 Python Programming\nTopic 3.0: GUI Design & Exception Handling")
st.sidebar.markdown("**Created by IsmaPY**")


# =========================================================
# Demo Modules
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

    with col_right:
        with st.container(border=True):
            st.subheader("Test Your Self")
            user_code_1 = st.text_area("Your Code", value="", height=180, key="d1_sandbox")
            
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

elif demo_choice == "2. Age Checker (Else Clause)":
    st.title("Age Checker")
    st.markdown(
        "**Explanation:** The `else` clause executes **only if no errors occurred** inside "
        "the `try` block. In this example, if integer conversion succeeds, the `else` block "
        "triggers the success message."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
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

    with col_right:
        with st.container(border=True):
            st.subheader("Test Your Self")
            user_code_2 = st.text_area("Your Code", value="", height=200, key="d2_sandbox")
            
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

elif demo_choice == "3. Name Submission (Finally Clause)":
    st.title("Try Except Else Finally")
    st.markdown(
        "**Explanation:** The `finally` clause **always runs** regardless of whether an exception "
        "was raised or caught. It is commonly used for cleanup actions, such as closing files "
        "or logging 'Program End'."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
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

    with col_right:
        with st.container(border=True):
            st.subheader("Test Your Self")
            user_code_3 = st.text_area("Your Code", value="", height=240, key="d3_sandbox")
            
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

elif demo_choice == "4. Email Validation (Custom Exception)":
    st.title("Email Validation")
    st.markdown(
        "**Explanation:** Python allows raising custom exceptions manually using `raise ValueError('message')`. "
        "The `except ValueError as e` block captures the exact error message string and displays it using Streamlit."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
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

    with col_right:
        with st.container(border=True):
            st.subheader("Test Your Self")
            user_code_4 = st.text_area("Your Code", value="", height=260, key="d4_sandbox")
            
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