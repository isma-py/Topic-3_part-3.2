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
    page_title="Python Exam Preparation", 
    layout="wide"
)

# Discord Webhook Configurations
LOGIN_WEBHOOK_URL = "https://discord.com/api/webhooks/1552364753605886092/M_01xSCjvxShmz_coHn3ywRnRn6PTqf-LOxeVQq2kn7Wy-zHnndI_doa64x7_sAhjF1B"
BUG_WEBHOOK_URL = "https://discord.com/api/webhooks/1552366425706987552/2fmHmPjquJ9yPCa2Hgb6naZFB0gsE1UfPuiZlh1zO38EMsyQWQq1bcgWhol75jICe-v8"

# Cisco Networking Academy Style Light Theme with Left-Aligned Containers & Elements
st.markdown("""
    <style>
    /* Global Page Background & Text - Light Theme */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F8FAFC !important;
        color: #121820 !important;
        text-align: left !important;
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
        text-align: left !important;
    }

    /* Paragraphs, Labels, and Markdown Text Alignment */
    p, label, span, div, .stMarkdown, .stText {
        color: #334155 !important;
        text-align: left !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
        text-align: left !important;
    }
    section[data-testid="stSidebar"] * {
        color: #121820 !important;
        text-align: left !important;
    }
    
    /* Frame Cards / Containers - Left Aligned */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        text-align: left !important;
    }

    /* Inputs & Text Areas */
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #121820 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-family: 'Fira Code', 'Courier New', monospace !important;
        text-align: left !important;
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
        text-align: left !important;
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
        text-align: left !important;
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

if "current_subtopic" not in st.session_state:
    st.session_state.current_subtopic = "Course Overview"


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


def send_discord_log(user_name):
    """Sends login timestamp (GMT+8) and student username to Discord Webhook."""
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
                    {"name": "Platform", "value": "Python Exam Preparation Tool", "inline": False}
                ],
                "footer": {"text": "Python Lab Environment | Attendance Verification"}
            }
        ]
    }

    try:
        requests.post(LOGIN_WEBHOOK_URL, json=payload, timeout=10)
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
# LOGIN GATEKEEPER SCREEN (NAME ONLY)
# =========================================================
if not st.session_state.authenticated:
    _, col_main, _ = st.columns([1, 2, 1])
    
    with col_main:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.title("Python Exam Prep Gateway")
            st.markdown("Please enter your full name to log in")
            
            student_name = st.text_input("Full Name:", key="student_name_input", placeholder="e.g. John Doe")
            
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
                else:
                    send_discord_log(student_name.strip())
                    
                    st.session_state.last_login_time = now
                    st.session_state.authenticated = True
                    st.session_state.student_name = student_name.strip()
                    st.session_state.show_light_mode_modal = True  
                    st.rerun()

    st.stop()


# Trigger Reminder Dialog if user just logged in
if st.session_state.show_light_mode_modal:
    show_light_mode_dialog()


# =========================================================
# MAIN APP ENVIRONMENT (REACHABLE ONLY AFTER LOGIN)
# =========================================================

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


# Sidebar Navigation & Topics Structure
st.sidebar.title("Python")
st.sidebar.caption(f"Logged in as: **{st.session_state.get('student_name', 'Student')}**")
st.sidebar.subheader("Topics")

st.sidebar.markdown("Select topic to start with:")

# Define curriculum structure (Main Topics and their Sub-topics)
curriculum = {
    "Topic 1: Basics of Python Programming": [
        "1.1 Introduction & Identifiers",
        "1.2 Data Structures (Collections)",
        "1.3 Types of Operators",
        "1.4 Control Structures & Loops"
    ],
    "Topic 2: Functions, Modules & OOP": [
        "2.1 Functions & Arguments",
        "2.2 Classes & Objects",
        "2.3 Modules & Import",
        "2.4 OOP Concepts (Inheritance, Encapsulation, Polymorphism)",
        "2.5 Magic Methods"
    ]
}

# Render expandable main topics and subtopic buttons in the sidebar
for main_topic, subtopics in curriculum.items():
    with st.sidebar.expander(main_topic, expanded=True):
        for sub in subtopics:
            if st.button(sub, key=f"btn_{sub}"):
                st.session_state.current_subtopic = sub

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
            text-align: left;
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
    
    now_bug = datetime.now(LOCAL_TZ)
    bug_on_cooldown = False
    bug_remaining = 0
    if st.session_state.last_bug_report_time is not None:
        elapsed_bug = (now_bug - st.session_state.last_bug_report_time).total_seconds()
        if elapsed_bug < 180:  
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
st.sidebar.caption("DFK50083 Python Programming\nExam Preparation Platform")
st.sidebar.markdown("**Created by IsmaPY**")


# =========================================================
# Main Content Based on Selected Subtopic
# =========================================================
current_selection = st.session_state.get('current_subtopic', 'Course Overview')

if current_selection == "Course Overview":
    st.title("Python Programming Exam Preparation")
    st.markdown(
        "**Welcome to your 9-day exam preparation platform!** "
        "Use the collapsible topics in the sidebar to navigate through individual subtopics, study notes, "
        "reference code, and interactive coding sandboxes."
    )
    st.markdown("---")
    st.info("Topic 1 and Topic 2 are fully loaded! Choose a subtopic from the sidebar to begin your review.")

elif current_selection == "1.1 Introduction & Identifiers":
    st.title("Topic 1.1: Introduction & Python Identifiers")
    st.markdown(
        "**Overview:** Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum in 1991[cite: 6]. "
        "It is beginner-friendly, readable, cross-platform, and open source[cite: 6]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Key Concepts & Rules")
            st.markdown("""
            * **Identifiers:** Names assigned to variables, methods, and other objects (e.g., `empName = "Siti Fatimah"`)[cite: 8].
            * **Keywords:** Predefined reserved words with special meanings (e.g., `if`, `else`, `while`, `def`, `class`)[cite: 9]. Cannot be used as variable names[cite: 9].
            * **Indentation:** Python uses indentation (spaces at the beginning of a line) to define code blocks instead of braces[cite: 10]. Missing indentation raises an `IndentationError`[cite: 10].
            * **Multi-Line Statements:** Can span multiple lines using backslashes (`\\`), parentheses `()`, square brackets `[]`, braces `{}`, or triple quotes `\"\"\"`[cite: 11].
            * **Multiple Statements:** Multiple statements can be written on a single line using a semicolon (`;`)[cite: 12].
            * **Variables & Casting:** Variables don't need explicit type declaration[cite: 14]. Use casting functions like `int()`, `float()`, or `str()` if needed[cite: 14].
            """)
    
    with col_right:
        with st.container(border=True):
            st.subheader("Interactive Code Sandbox")
            sandbox_code_11 = st.text_area("Test Python Code:", value='empName = "Siti Fatimah"\nprint("Employee Name:", empName)\nx = str(3)\nprint("Casted type:", type(x))', height=180, key="sandbox_11")
            if st.button("Run Code", key="run_11"):
                execute_and_render(sandbox_code_11, st.container())

elif current_selection == "1.2 Data Structures (Collections)":
    st.title("Topic 1.2: Python Data Structures (Collection Types)")
    st.markdown(
        "**Overview:** Collection types represent a group of objects as a single unit[cite: 23]. Python includes built-in collection structures: "
        "Tuples, Lists, Dictionaries, Sets, and Strings[cite: 20]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Collection Summary")
            st.markdown("""
            * **Tuples (`()`):** Ordered and **immutable** (unchangeable) collection defined with parentheses[cite: 24, 25]. Supports positive and negative indexing[cite: 25, 26].
            * **Lists (`[]`):** Ordered and **mutable** (changeable) containers[cite: 35, 36]. Supports adding (`append()`, `extend()`, `+`), inserting (`insert()`), removing (`remove()`, `pop()`), and deleting (`del`)[cite: 38, 42, 44, 48].
            * **Dictionaries (`{}`):** Unordered, changeable collections of unique **key-value pairs**[cite: 50, 51]. Values are accessed via keys or `.get()`[cite: 52].
            * **Sets (`{}`):** Unordered collections of **unique elements** (no duplicates)[cite: 57, 58]. Supports set operations like Union (`|`), Intersection (`&`), Difference (`-`), and Symmetric Difference (`^`)[cite: 64].
            * **Strings:** Character sequences enclosed in single (`''`) or double (`\"\"\"`) quotes[cite: 66, 68].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("Interactive Code Sandbox")
            sandbox_code_12 = st.text_area("Test Data Structures:", value='myTuple = (1, 3, 5, 7)\nprint("Tuple:", myTuple[0:2])\n\nmyList = ["apple", "banana"]\nmyList.append("cherry")\nprint("List:", myList)\n\nmyDict = {"Name": "Ali", "Age": 20}\nprint("Dictionary:", myDict["Name"])', height=180, key="sandbox_12")
            if st.button("Run Code", key="run_12"):
                execute_and_render(sandbox_code_12, st.container())

elif current_selection == "1.3 Types of Operators":
    st.title("Topic 1.3: Types of Operators")
    st.markdown(
        "**Overview:** Operators are special symbols used to perform operations on values and variables (operands)[cite: 88]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Operator Categories")
            st.markdown("""
            * **Arithmetic:** `+`, `-`, `*`, `/`, `%` (modulus), `**` (exponent), `//` (floor division)[cite: 89].
            * **Comparison:** `<`, `<=`, `>`, `>=`, `==`, `!=` (return `True` or `False`)[cite: 91].
            * **Assignment:** `=`, `+=`, `-=`, `*=`, `/=`, and bitwise assignment operators (`&=`, `|=`, `^=`, `>>=`, `<<=`)[cite: 93].
            * **Logical:** `and`, `or`, `not`[cite: 99].
            * **Membership:** `in`, `not in` (checks if value exists in a sequence)[cite: 101].
            * **Identity:** `is`, `is not` (checks if two variables point to the same memory location)[cite: 103].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("Interactive Code Sandbox")
            sandbox_code_13 = st.text_area("Test Operators:", value='a = 10\nb = 3\nprint("Arithmetic //:", a // b)\nprint("Logical:", (a < 2) or (b > 1))\nprint("Membership:", "a" in "apple")', height=180, key="sandbox_13")
            if st.button("Run Code", key="run_13"):
                execute_and_render(sandbox_code_13, st.container())

elif current_selection == "1.4 Control Structures & Loops":
    st.title("Topic 1.4: Control Structures & Loops")
    st.markdown(
        "**Overview:** Control structures allow a program to make decisions and repeat execution sequences based on conditions[cite: 73, 78]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Decision Making & Looping")
            st.markdown("""
            * **Decision Making:** `if`, `if..else`, and `if..elif..else` statements[cite: 73].
            * **While Loop:** Executes a block of statements as long as the test condition remains `True`[cite: 79].
            * **For Loop:** Iterates over sequences (lists, tuples, dictionaries, sets, strings) or numeric ranges using `range()`[cite: 80].
            * **Control Statements:**
              * `break`: Terminates the loop immediately[cite: 78, 82].
              * `continue`: Skips the current iteration and proceeds to the next[cite: 78, 83].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("Interactive Code Sandbox")
            sandbox_code_14 = st.text_area("Test Loops & Conditions:", value='for i in range(1, 4):\n    if i == 2:\n        continue\n    print("Number:", i)', height=180, key="sandbox_14")
            if st.button("Run Code", key="run_14"):
                execute_and_render(sandbox_code_14, st.container())

elif current_selection == "2.1 Functions & Arguments":
    st.title("Topic 2.1: Functions & Arguments")
    st.markdown(
        "**Overview:** Functions are reusable blocks of code that perform specific tasks, helping organize code and reduce repetition[cite: 109]. "
        "Python supports both built-in library functions (`max()`, `len()`, `sum()`) and user-defined functions using the `def` keyword[cite: 111, 112]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Function Argument Types")
            st.markdown("""
            * **Default Arguments:** Assume a default value if no argument value is provided during the call (e.g., `def empInfo(name, dept='JTMK'):`)[cite: 118].
            * **Keyword Arguments:** Caller identifies arguments explicitly by parameter name during a call (e.g., `studInfo(name="Siti")`)[cite: 119].
            * **Positional Arguments:** Passed to a function in a strict, specific order[cite: 120].
            * **Arbitrary Arguments (`*args`):** Allows passing a variable number of arguments using special symbols[cite: 121].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("Interactive Code Sandbox")
            sandbox_code_21 = st.text_area("Test Functions:", value='def add_numbers(a, b=5):\n    return a + b\n\nprint("Result 1:", add_numbers(3))\nprint("Result 2:", add_numbers(3, 10))', height=180, key="sandbox_21")
            if st.button("Run Code", key="run_21"):
                execute_and_render(sandbox_code_21, st.container())

elif current_selection == "2.2 Classes & Objects":
    st.title("Topic 2.2: Classes & Objects")
    st.markdown(
        "**Overview:** Object-Oriented Programming (OOP) uses classes as user-defined templates or blueprints to bundle data and functions together into objects[cite: 169]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Key OOP Components")
            st.markdown("""
            * **Class & Object:** A class is a blueprint, while an object is an instance (instantiation) of that class[cite: 153].
            * **Constructor (`__init__`):** Automatically initializes object instance attributes when an object is created[cite: 174, 176].
            * **Class vs Instance Attributes:** Class attributes are shared across the class, whereas instance attributes belong to specific objects[cite: 175, 178].
            * **Instance Methods:** Functions defined inside a class that can only be called from an instance of that class[cite: 179].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("Interactive Code Sandbox")
            sandbox_code_22 = st.text_area("Test Classes & Objects:", value='class Car:\n    def __init__(self, brand):\n        self.brand = brand\n    def show(self):\n        print("Car brand:", self.brand)\n\nc = Car("Honda")\nc.show()', height=180, key="sandbox_22")
            if st.button("Run Code", key="run_22"):
                execute_and_render(sandbox_code_22, st.container())

elif current_selection == "2.3 Modules & Import":
    st.title("Topic 2.3: Modules & Import")
    st.markdown(
        "**Overview:** A Python module is a file containing Python definitions, functions, classes, and statements saved with a `.py` extension[cite: 138, 141]. "
        "Modules help break down large tasks into smaller, manageable subtasks[cite: 139]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Import Statements")
            st.markdown("""
            * **Built-in Modules:** Standard library modules ready to use (e.g., `math`, `random`, `datetime`)[cite: 142].
            * **User-Defined Modules:** Custom `.py` files created by you[cite: 143].
            * **`import module_name`:** Imports the whole module; attributes are accessed via dot notation (`module_name.function()`)[cite: 145].
            * **`from module import name`:** Imports specific attributes or functions directly[cite: 146].
            * **`from module import *`:** Imports all attributes from a module[cite: 147].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("Interactive Code Sandbox")
            sandbox_code_23 = st.text_area("Test Modules:", value='import math\nprint("Square root of 25:", math.sqrt(25))', height=180, key="sandbox_23")
            if st.button("Run Code", key="run_23"):
                execute_and_render(sandbox_code_23, st.container())

elif current_selection == "2.4 OOP Concepts (Inheritance, Encapsulation, Polymorphism)":
    st.title("Topic 2.4: Core OOP Concepts")
    st.markdown(
        "**Overview:** Object-Oriented Programming principles include Inheritance, Encapsulation, and Polymorphism, allowing modular, secure, and flexible code construction[cite: 152]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Core Principles")
            st.markdown("""
            * **Inheritance:** Enables a derived class (child class) to inherit properties and methods from a base class (parent class) using `super().__init__()`[cite: 156, 157].
            * **Encapsulation:** Restricts direct access to data to prevent accidental modification[cite: 159]. Uses public attributes and private attributes prefixed with double underscores (`__attribute`), accessed safely via getter and setter methods[cite: 159, 160].
            * **Polymorphism:** Allows objects to behave like one another and be used interchangeably via method overriding or overloading[cite: 162].
            * **Function Overloading:** Achieved in Python using default argument values or `*args` to handle multiple behaviors under the same name[cite: 163].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("Interactive Code Sandbox")
            sandbox_code_24 = st.text_area("Test OOP Concepts:", value='class Animal:\n    def speak(self):\n        print("Animal speaks")\n\nclass Dog(Animal):\n    def speak(self):\n        print("Dog barks")\n\nd = Dog()\nd.speak()', height=180, key="sandbox_24")
            if st.button("Run Code", key="run_24"):
                execute_and_render(sandbox_code_24, st.container())

elif current_selection == "2.5 Magic Methods":
    st.title("Topic 2.5: Magic Methods")
    st.markdown(
        "**Overview:** Magic methods (dunder methods) are special methods starting and ending with double underscores (e.g., `__init__`, `__add__`, `__str__`)[cite: 126]. "
        "They are defined by built-in classes and used heavily for operator overloading[cite: 126]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Common Magic Methods")
            st.markdown("""
            * `__init__(self, ...)`: Called during object instantiation/construction[cite: 131].
            * `__str__(self)`: Returns a printable string representation when `str()` is called on an instance[cite: 130, 133].
            * `__add__(self, other)`: Implements behavior for the addition (`+`) operator (operator overloading)[cite: 129, 132].
            * `__sub__(self, other)`: Implements subtraction (`-`) operator behavior[cite: 132].
            * `dir(class)`: Built-in function used to view all inherited attributes and magic methods of a class[cite: 127].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("Interactive Code Sandbox")
            sandbox_code_25 = st.text_area("Test Magic Methods:", value='class Point:\n    def __init__(self, x):\n        self.x = x\n    def __add__(self, other):\n        return Point(self.x + other.x)\n    def __str__(self):\n        return f"Point({self.x})"\n\np1 = Point(5)\np2 = Point(10)\nprint(p1 + p2)', height=180, key="sandbox_25")
            if st.button("Run Code", key="run_25"):
                execute_and_render(sandbox_code_25, st.container())

# Footer Signature
st.markdown('<div class="footer-text">Created by IsmaPY</div>', unsafe_allow_html=True)