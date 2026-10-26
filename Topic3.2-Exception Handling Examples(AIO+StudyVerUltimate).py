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
    page_title="Python Exam Preparation & Testing", 
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
        "your progress or quiz answers. Please remember to record your scores manually if needed!"
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
    ],
    "Topic 3: GUI Design & Exception Handling": [
        "3.1 Introduction to GUI & Streamlit UI",
        "3.2 User Events & Interactive Widgets",
        "3.3 Exception Handling (Try & Except)",
        "3.4 Exception Handling (Else & Finally)"
    ],
    "Topic 4: Matrix Processing & Data Analysis": [
        "4.1 NumPy ndarray & Creation Routines",
        "4.2 Indexing, Slicing & Array Manipulation",
        "4.3 Matplotlib Data Visualization",
        "4.4 Pandas Series & DataFrames",
        "4.5 Pandas Data Pre-Processing"
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
# Main Content Based on Selected Subtopic (Left: Notes | Right: Testing Quiz)
# =========================================================
current_selection = st.session_state.get('current_subtopic', 'Course Overview')

if current_selection == "Course Overview":
    st.title("Python Programming Exam Preparation")
    st.markdown(
        "**Welcome to your exam preparation platform!** "
        "Use the collapsible topics in the sidebar to navigate through individual subtopics, study notes, "
        "and the **Understanding Quiz** on the right side of each page."
    )
    st.markdown("---")
    st.info("Topics 1, 2, 3, and 4 are fully loaded with study notes and interactive testing modules!")

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
            st.subheader("🧠 Understanding Check: Quiz 1.1")
            st.markdown("Test your knowledge on identifiers and syntax rules:")
            q1 = st.radio("Which of the following is a valid Python keyword that cannot be used as an identifier?", ["name", "class", "value", "total"], key="q1_1")
            if st.button("Check Answer", key="btn_q1_1"):
                if q1 == "class":
                    st.success("Correct! `class` is a reserved keyword in Python[cite: 9].")
                else:
                    st.error("Incorrect. `class` is a reserved keyword[cite: 9].")

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
            st.subheader("🧠 Understanding Check: Quiz 1.2")
            st.markdown("Test your knowledge on Python collections:")
            q2 = st.radio("Which collection type is ordered and immutable?", ["List []", "Tuple ()", "Dictionary {}", "Set {}"], key="q1_2")
            if st.button("Check Answer", key="btn_q1_2"):
                if q2 == "Tuple ()":
                    st.success("Correct! Tuples are ordered and immutable collections defined with parentheses[cite: 24, 25].")
                else:
                    st.error("Incorrect. Tuples are immutable, unlike lists or dictionaries[cite: 25, 36].")

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
            st.subheader("🧠 Understanding Check: Quiz 1.3")
            st.markdown("Test your knowledge on operators:")
            q3 = st.radio("What does the floor division operator (`//`) do?", ["Returns remainder", "Performs exponentiation", "Rounds down division to nearest integer", "Returns float division"], key="q1_3")
            if st.button("Check Answer", key="btn_q1_3"):
                if q3 == "Rounds down division to nearest integer":
                    st.success("Correct! Floor division (`//`) divides operands and floors the result to the nearest integer[cite: 89].")
                else:
                    st.error("Incorrect. Floor division (`//`) performs integer division rounding down[cite: 89].")

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
            st.subheader("🧠 Understanding Check: Quiz 1.4")
            st.markdown("Test your knowledge on control statements:")
            q4 = st.radio("Which control statement skips the current iteration and proceeds to the next?", ["break", "continue", "pass", "exit"], key="q1_4")
            if st.button("Check Answer", key="btn_q1_4"):
                if q4 == "continue":
                    st.success("Correct! `continue` skips the current iteration and jumps to the next loop cycle[cite: 78, 83].")
                else:
                    st.error("Incorrect. `continue` is used to skip the current iteration[cite: 83].")

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
            st.subheader("🧠 Understanding Check: Quiz 2.1")
            st.markdown("Test your knowledge on functions:")
            q5 = st.radio("Which symbol is used for arbitrary arguments in Python functions?", ["&", "*", "#", "%"], key="q2_1")
            if st.button("Check Answer", key="btn_q2_1"):
                if q5 == "*":
                    st.success("Correct! `*args` allows passing a variable number of positional arguments[cite: 121].")
                else:
                    st.error("Incorrect. `*` is used for arbitrary arguments (`*args`)[cite: 121].")

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
            st.subheader("🧠 Understanding Check: Quiz 2.2")
            st.markdown("Test your knowledge on classes and objects:")
            q6 = st.radio("What is the name of the constructor method in Python classes?", ["__main__", "__init__", "__start__", "__new_obj__"], key="q2_2")
            if st.button("Check Answer", key="btn_q2_2"):
                if q6 == "__init__":
                    st.success("Correct! `__init__` is the standard constructor method in Python classes[cite: 174, 176].")
                else:
                    st.error("Incorrect. `__init__` is used to initialize object attributes[cite: 176].")

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
            st.subheader("🧠 Understanding Check: Quiz 2.3")
            st.markdown("Test your knowledge on modules:")
            q7 = st.radio("How do you import a specific function from a module in Python?", ["include module.function", "import module.function", "from module import function", "get module function"], key="q2_3")
            if st.button("Check Answer", key="btn_q2_3"):
                if q7 == "from module import function":
                    st.success("Correct! `from module import name` imports specific attributes or functions directly[cite: 146].")
                else:
                    st.error("Incorrect. The correct syntax is `from module import name`[cite: 146].")

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
            st.subheader("🧠 Understanding Check: Quiz 2.4")
            st.markdown("Test your knowledge on OOP principles:")
            q8 = st.radio("Which OOP principle restricts direct access to data using private attributes (`__attribute`)?", ["Inheritance", "Polymorphism", "Encapsulation", "Abstraction"], key="q2_4")
            if st.button("Check Answer", key="btn_q2_4"):
                if q8 == "Encapsulation":
                    st.success("Correct! Encapsulation restricts direct data access to protect object state[cite: 159].")
                else:
                    st.error("Incorrect. Encapsulation is responsible for data hiding/restricting access[cite: 159].")

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
            st.subheader("🧠 Understanding Check: Quiz 2.5")
            st.markdown("Test your knowledge on magic methods:")
            q9 = st.radio("Which magic method defines the behavior of the addition operator (`+`)?", ["__init__", "__add__", "__str__", "__sum__"], key="q2_5")
            if st.button("Check Answer", key="btn_q2_5"):
                if q9 == "__add__":
                    st.success("Correct! `__add__` overloads the `+` operator for custom objects[cite: 129, 132].")
                else:
                    st.error("Incorrect. `__add__` is used for the addition operator[cite: 132].")

elif current_selection == "3.1 Introduction to GUI & Streamlit UI":
    st.title("Topic 3.1: Introduction to GUI & Streamlit UI")
    st.markdown(
        "**Overview:** A Graphical User Interface (GUI) allows users to interact visually using buttons, text boxes, and sliders instead of console commands[cite: 184]. "
        "Streamlit is a Python framework that turns Python scripts into interactive web applications without HTML, CSS, or JavaScript[cite: 186]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("GUI Frameworks & Streamlit Setup")
            st.markdown("""
            * **GUI Options:** Tkinter (built-in), PyQt / PySide, Streamlit (web-based), and Kivy (cross-platform/mobile)[cite: 184].
            * **Installation:** Install Streamlit via terminal using `pip install streamlit` or `python -m pip install streamlit`[cite: 186].
            * **Creating & Running:** Save your file as `app.py` and run it in the terminal using `streamlit run app.py`[cite: 187, 188].
            * **Deployment:** Public GitHub repositories containing `app.py` and `requirements.txt` can be deployed on Streamlit Community Cloud[cite: 189, 190, 191].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("🧠 Understanding Check: Quiz 3.1")
            st.markdown("Test your knowledge on Streamlit execution:")
            q10 = st.radio("What command is used in the terminal to run a Streamlit app script?", ["python app.py", "streamlit run app.py", "start streamlit app.py", "run streamlit"], key="q3_1")
            if st.button("Check Answer", key="btn_q3_1"):
                if q10 == "streamlit run app.py":
                    st.success("Correct! `streamlit run app.py` launches the application in your web browser[cite: 188].")
                else:
                    st.error("Incorrect. Streamlit apps are launched using `streamlit run app.py`[cite: 188].")

elif current_selection == "3.2 User Events & Interactive Widgets":
    st.title("Topic 3.2: User Events & Interactive Widgets")
    st.markdown(
        "**Overview:** Streamlit automatically updates and reruns the app whenever a user interacts with a widget[cite: 193]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Common Interactive Widgets")
            st.markdown("""
            * **Text Input (`st.text_input`):** Captures single-line text input from users[cite: 193].
            * **Button (`st.button`):** Triggers actions when clicked[cite: 194].
            * **Checkbox (`st.checkbox`):** Allows boolean true/false toggle options[cite: 195].
            * **Radio Buttons (`st.radio`):** Selects a single option from a list[cite: 196].
            * **Selectbox / Dropdown (`st.selectbox`):** Selects an item from a drop-down menu list[cite: 197].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("🧠 Understanding Check: Quiz 3.2")
            st.markdown("Test your knowledge on Streamlit widgets:")
            q11 = st.radio("How does Streamlit respond when a user interacts with a widget?", ["Nothing happens until page refresh", "It automatically reruns the Python script", "It opens a new tab", "It prompts for password"], key="q3_2")
            if st.button("Check Answer", key="btn_q3_2"):
                if q11 == "It automatically reruns the Python script":
                    st.success("Correct! Streamlit automatically updates and reruns whenever a widget is interacted with[cite: 193].")
                else:
                    st.error("Incorrect. Streamlit automatically reruns the script on widget interaction[cite: 193].")

elif current_selection == "3.3 Exception Handling (Try & Except)":
    st.title("Topic 3.3: Exception Handling (Try & Except)")
    st.markdown(
        "**Overview:** Exception handling allows programs to catch and manage runtime errors gracefully instead of crashing, making code robust and user-friendly[cite: 202]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Try and Except Blocks")
            st.markdown("""
            * **`try` Block:** Used to test and check a block of code for errors during execution[cite: 204]. Executes when there are no errors[cite: 204].
            * **`except` Block:** Executes whenever the program encounters an error in the preceding `try` block[cite: 204].
            * **Catching Specific Errors:** You can catch specific exceptions like `ValueError` or `ZeroDivisionError` to display customized error messages[cite: 200, 205].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("🧠 Understanding Check: Quiz 3.3")
            st.markdown("Test your knowledge on exception handling:")
            q12 = st.radio("When does the code inside an `except` block execute?", ["Always", "When there is no error in the try block", "Whenever an error occurs in the preceding try block", "Only at the end of the script"], key="q3_3")
            if st.button("Check Answer", key="btn_q3_3"):
                if q12 == "Whenever an error occurs in the preceding try block":
                    st.success("Correct! The `except` block executes whenever an error occurs in the `try` block[cite: 204].")
                else:
                    st.error("Incorrect. The `except` block handles errors encountered in the `try` block[cite: 204].")

elif current_selection == "3.4 Exception Handling (Else & Finally)":
    st.title("Topic 3.4: Exception Handling (Else & Finally)")
    st.markdown(
        "**Overview:** Advanced exception handling blocks (`else` and `finally`) provide precise control over code execution flow depending on whether errors occurred[cite: 207, 210]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Else & Finally Clauses")
            st.markdown("""
            * **`else` Clause:** Defines a block of code to be executed **only if no errors were raised** in the `try` block[cite: 207].
            * **`finally` Clause:** Always executes after the `try` and `except` blocks terminate, **regardless** of whether an error occurred or not[cite: 210].
            * **Raising Exceptions (`raise`):** Used to manually trigger custom exceptions (e.g., `raise ValueError("Invalid Email")`)[cite: 212, 213].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("🧠 Understanding Check: Quiz 3.4")
            st.markdown("Test your knowledge on `else` and `finally`:")
            q13 = st.radio("Which block is guaranteed to run regardless of whether an exception occurs or not?", ["try", "except", "else", "finally"], key="q3_4")
            if st.button("Check Answer", key="btn_q3_4"):
                if q13 == "finally":
                    st.success("Correct! The `finally` block executes regardless of whether an error occurred[cite: 210].")
                else:
                    st.error("Incorrect. The `finally` block executes unconditionally[cite: 210].")

elif current_selection == "4.1 NumPy ndarray & Creation Routines":
    st.title("Topic 4.1: NumPy ndarray & Creation Routines")
    st.markdown(
        "**Overview:** NumPy (Numerical Python) is the core library for matrix processing in Python[cite: 218, 226]. "
        "Its central data structure is `ndarray` (n-dimensional array), which is significantly faster and more memory-efficient than Python lists because elements are stored in contiguous memory[cite: 226]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Array Attributes & Creation Functions")
            st.markdown("""
            * **Core Attributes:** `.shape` (rows, columns)[cite: 232], `.ndim` (number of dimensions)[cite: 232], `.size` (total elements)[cite: 232], `.dtype` (data type)[cite: 232], and `.nbytes` (total memory)[cite: 232].
            * **`np.zeros(shape)` / `np.ones(shape)`:** Creates arrays filled with zeros or ones[cite: 235].
            * **`np.full(shape, value)`:** Creates an array filled with a specified value[cite: 235].
            * **`np.eye(n)`:** Generates an $n \times n$ identity matrix[cite: 235].
            * **`np.arange(start, stop, step)`:** Returns evenly spaced values within a given range[cite: 235].
            * **`np.linspace(start, stop, num)`:** Generates a specified number of evenly spaced values[cite: 235].
            * **`np.random.randint(low, high, size)`:** Generates random integers within a range[cite: 235].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("🧠 Understanding Check: Quiz 4.1")
            st.markdown("Test your knowledge on NumPy arrays:")
            q14 = st.radio("Why are NumPy `ndarray` objects faster than standard Python lists?", ["They use less RAM", "They are stored in contiguous memory", "They only hold strings", "They run on multiple computers"], key="q4_1")
            if st.button("Check Answer", key="btn_q4_1"):
                if q14 == "They are stored in contiguous memory":
                    st.success("Correct! NumPy arrays are faster and more efficient because data is stored in contiguous memory[cite: 226].")
                else:
                    st.error("Incorrect. Contiguous memory allocation makes NumPy arrays faster[cite: 226].")

elif current_selection == "4.2 Indexing, Slicing & Array Manipulation":
    st.title("Topic 4.2: Indexing, Slicing & Array Manipulation")
    st.markdown(
        "**Overview:** NumPy allows precise data extraction via multi-dimensional indexing and slicing (`arr[row, col]` and `start:stop:step`), "
        "along with structural manipulation without altering underlying data[cite: 238, 240, 244]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Manipulation & Slicing Operations")
            st.markdown("""
            * **Indexing (`arr[row, col]`):** Accesses specific elements; negative indices count from the end[cite: 238, 239].
            * **Slicing (`arr[start:stop, start:stop]`):** Extracts portions of arrays (stop index is exclusive)[cite: 240, 241].
            * **`reshape(shape)`:** Changes array dimensions without altering data[cite: 244, 245].
            * **`flatten()`:** Converts a multi-dimensional array into a 1D array[cite: 244, 245].
            * **`transpose()` or `.T`:** Flips rows and columns[cite: 244, 245].
            * **Stacking & Concatenation:** `np.hstack()`, `np.vstack()`, and `np.concatenate(axis=0/1)` combine arrays horizontally or vertically[cite: 244, 246].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("🧠 Understanding Check: Quiz 4.2")
            st.markdown("Test your knowledge on array manipulation:")
            q15 = st.radio("Which NumPy function changes an array's shape without modifying its underlying data?", ["flatten()", "reshape()", "transpose()", "resize()"], key="q4_2")
            if st.button("Check Answer", key="btn_q4_2"):
                if q15 == "reshape()":
                    st.success("Correct! `reshape()` changes the array shape without changing the data[cite: 244, 245].")
                else:
                    st.error("Incorrect. `reshape()` is used to modify array dimensions[cite: 245].")

elif current_selection == "4.3 Matplotlib Data Visualization":
    st.title("Topic 4.3: Matplotlib Data Visualization")
    st.markdown(
        "**Overview:** Matplotlib is a powerful Python visualization library that integrates seamlessly with NumPy arrays "
        "to plot mathematical functions, inspect trends, and present analytical results[cite: 221]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Key Plotting Functions")
            st.markdown("""
            * **Installation:** Install via terminal using `pip install matplotlib`[cite: 222].
            * **Line Plots (`plt.plot(x, y)`):** Connects data points with lines; supports custom markers like `marker='o'`[cite: 222, 223].
            * **Scatter Plots (`plt.scatter(x, y)`):** Displays individual data points to show correlation between variables (e.g., exam score comparisons)[cite: 224].
            * **Customization:** Use `plt.title()`, `plt.xlabel()`, `plt.ylabel()`, `plt.grid(True)`, and `plt.ylim()` to format graphs for readability[cite: 222, 223, 224].
            * **Display:** `plt.show()` renders the graph window[cite: 222, 223, 224].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("🧠 Understanding Check: Quiz 4.3")
            st.markdown("Test your knowledge on Matplotlib:")
            q16 = st.radio("Which Matplotlib function displays grid lines on a graph for easier reading?", ["plt.show()", "plt.grid(True)", "plt.lines()", "plt.box()"], key="q4_3")
            if st.button("Check Answer", key="btn_q4_3"):
                if q16 == "plt.grid(True)":
                    st.success("Correct! `plt.grid(True)` enables grid lines on the plot[cite: 222, 223].")
                else:
                    st.error("Incorrect. `plt.grid(True)` is used to display grid lines[cite: 223].")

elif current_selection == "4.4 Pandas Series & DataFrames":
    st.title("Topic 4.4: Pandas Series & DataFrames")
    st.markdown(
        "**Overview:** Pandas is a powerful Python library for data analysis and manipulation[cite: 254]. "
        "It provides two primary data structures: **Series** (1D labeled array) and **DataFrame** (2D tabular structure with rows and columns, similar to an Excel table)[cite: 255, 260]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Series & DataFrame Operations")
            st.markdown("""
            * **Series (`pd.Series`):** A one-dimensional labeled array where values can be accessed, updated, added, or dropped by label index[cite: 256, 260].
            * **DataFrame (`pd.DataFrame`):** A 2D table created using dictionaries or imported files[cite: 257, 258].
            * **Column Selection:** Access single columns (`df['col']`) or multiple columns (`df[['col1', 'col2']]`)[cite: 257, 258, 262].
            * **Row Selection:** Use `.iloc[index]` for integer position indexing or `.loc[label, col]` for label-based lookup[cite: 262].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("🧠 Understanding Check: Quiz 4.4")
            st.markdown("Test your knowledge on Pandas structures:")
            q17 = st.radio("What best describes a Pandas DataFrame?", ["A 1D labeled array", "A 2D table with labeled rows and columns", "An immutable tuple", "A 3D tensor"], key="q4_4")
            if st.button("Check Answer", key="btn_q4_4"):
                if q17 == "A 2D table with labeled rows and columns":
                    st.success("Correct! A DataFrame is a 2D table-like structure with rows and columns similar to Excel[cite: 255, 260].")
                else:
                    st.error("Incorrect. DataFrames are 2D tabular data structures[cite: 260].")

elif current_selection == "4.5 Pandas Data Pre-Processing":
    st.title("Topic 4.5: Pandas Data Pre-Processing")
    st.markdown(
        "**Overview:** Data pre-processing involves cleaning, transforming, and organizing raw data to improve accuracy and quality before analysis[cite: 263]."
    )
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.container(border=True):
            st.subheader("Pre-Processing Methods")
            st.markdown("""
            * **Data Importing:** Load external files efficiently using `pd.read_csv()` or `pd.read_excel()`[cite: 265, 266].
            * **Duplicates:** Detect duplicate records with `.duplicated()` and remove them using `.drop_duplicates()`[cite: 267, 268].
            * **Missing Values:** Identify missing values (`NaN`) with `.isnull().sum()` and fill or drop them using `.fillna()` or `.dropna()`[cite: 269, 270].
            * **Dropping & Filtering:** Remove unnecessary rows/columns with `.drop()` or select specific subsets using conditional filters[cite: 271, 272, 273, 274].
            * **Sorting & Grouping:** Order data using `.sort_values()` and aggregate categories with `.groupby()`[cite: 275, 276, 277, 278].
            * **Resampling & Concatenation:** Change time-series frequency using `.resample()` and merge datasets with `pd.concat()`[cite: 279, 280, 281, 282].
            """)
            
    with col_right:
        with st.container(border=True):
            st.subheader("🧠 Understanding Check: Quiz 4.5")
            st.markdown("Test your knowledge on data pre-processing:")
            q18 = st.radio("Which Pandas method is used to fill missing (`NaN`) values?", ["drop_duplicates()", "fillna()", "groupby()", "resample()"], key="q4_5")
            if st.button("Check Answer", key="btn_q4_5"):
                if q18 == "fillna()":
                    st.success("Correct! `fillna()` is used to replace missing values with specified values or statistics[cite: 270].")
                else:
                    st.error("Incorrect. `fillna()` is used for handling missing values[cite: 270].")

# Footer Signature
st.markdown('<div class="footer-text">Created by IsmaPY</div>', unsafe_allow_html=True)